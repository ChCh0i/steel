import angr
import claripy
import logging

# logging.getLogger('angr').setLevel(logging.ERROR)

# target = [0xB0, 0xBF, 0x5D, 0x21, 0xB3, 0x22, 0xEF, 0xAF, 0x27, 0x65, 0x93, 0x41, 0x73, 0x86, 0x3E, 0x60
# , 0x98, 0xCF, 0x37, 0xDD, 0xD1, 0x82, 0xD7, 0x78, 0x36, 0xA5, 0xB7, 0x45, 0xE6, 0x23, 0x4D, 0xC8
# , 0x7B, 0x46, 0x97, 0x95, 0xF5, 0x35, 0xAB, 0x2B, 0xFD, 0x05, 0x4C, 0xD9, 0x89, 0x72, 0x2D, 0x9E
# , 0xBC, 0x2E, 0x3D, 0x4A, 0x7D, 0x05, 0x44, 0xBB, 0xC8, 0xD5, 0xC1, 0x2A, 0x64, 0xE9, 0x90, 0x41
# , 0x16, 0x7E, 0x2A, 0x8B, 0x9B, 0xA0, 0xB8, 0x51, 0xD2, 0x73, 0xFA, 0xD9, 0x73, 0xD9, 0xFF, 0x94
# , 0x0D, 0x51, 0x3B, 0xC7, 0x35, 0xBD, 0x85, 0x7F]

FIND_ARRAY = [0x401CD0, 0x4024FC, 0x402D20, 0x40353F, 0x403D9A, 0x4045AF, 0x404DD1, 0x40561B, 0x405E44, 0x406675, 0x406E8A, 
                0x4076A2, 0x407EC6, 0x4086EA, 0x408F48, 0x409783, 0x409FBB, 0x40A7EE, 0x40B012, 0x40B840, 0x40C08C, 0x40C8EC]

assert(len(FIND_ARRAY) == 22)

ANTI_FUNC = 0x4013A6
FLAG = ""

def anti_func_bypass(state):
    state.regs = state.regs.rdi + state.regs.rsi 
    
def case_func(i, proj, inputs):
    global FLAG
    input_4_bytes = claripy.Concat(inputs[i], inputs[i+1], inputs[i+2], inputs[i+3])
    
    init_state = proj.factory.call_state(0x40147B, input_4_bytes, i)

    for j in range(4):
        byte = input_4_bytes[(j+1)*8-1:j*8]
        init_state.solver.add(byte > 0x20, byte <= 0x7E)

    proj.hook(ANTI_FUNC, anti_func_bypass, replace=True)
    simgr = proj.factory.simgr(init_state)

    simgr.explore(find=FIND_ARRAY[i], aviod=0x40C8FE)

    if simgr.found:
        # for solution_state in simgr.found:
        solution_state = simgr.found[0]
        maybe_flag = solution_state.solver.eval(input_4_bytes)
        print(f"[+] Solution Found : {maybe_flag}, {maybe_flag:8x}")
        print('Solution found!')
        FLAG += f"{maybe_flag:8x}"
    elif simgr.errored:
        print('An error occurred during exploration.')
        for error_state in simgr.errored:
            print('Error message:', error_state.error)
    elif simgr.deadended:
        print('Exploration reached a dead end.')
    else:
        print('No solution found.')
def main(args):
    BIN = args.binary
    proj = angr.Project(BIN, load_options={'auto_load_libs': False})

    inputs = [claripy.BVS('input_%d' % i, 8) for i in range(88)]
    assert(len(inputs) == 88)

    for i in range(22): #22
        case_func(i, proj, inputs)
    
    print(FLAG)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("binary", type=str)
    # parser.add_argument("passcode", type=(lambda x: int(x, 16)))
    args = parser.parse_args()
    main(args)