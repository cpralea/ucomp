import argparse
import ctypes


VM_LIB = 'vm/build/vm.so'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='VM wrapper.')
    parser.add_argument('program', metavar='HEX', type=str, nargs=1, \
                        help='the program to execute')
    parser.add_argument('-m', '--memory', metavar='MEM', type=str, dest='memory', \
                        required=False, default=4, \
                        help='the size of memory to use (in MiB); defaults to 4')
    return parser.parse_args()


def run():
    args = parse_args()

    program: bytes
    with open(args.program[0], mode='r', encoding='utf-8') as hex_file:
        program = bytes.fromhex(' '.join([line.strip() for line in hex_file]))
    ram_size_mb: int = args.memory

    ctypes.cdll.LoadLibrary(VM_LIB).vm_run(program, len(program), ram_size_mb)


run()
