import argparse
import ctypes

from enum import IntEnum, unique


VM_LIB = 'vm.so'


@unique
class ExecType(IntEnum):
    INTERPRETER = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='VM wrapper.')
    parser.add_argument('program', metavar='HEX', type=str, nargs=1,
                        help='the program to execute')
    parser.add_argument('-m', '--memory', metavar='MEM', type=str, dest='memory',
                        required=False, default=4,
                        help='the size of memory to use (in MiB); defaults to 4')
    parser.add_argument('-e', '--execution-type', metavar='EXEC_TYPE', dest='exec_type',
                        required=False, choices=['INTERPRETER'], default='INTERPRETER',
                        help='''the execution type; defaults to INTERPRETER;
                                possible values: INTERPRETER''')
    parser.add_argument('-d', '--debug', dest='debug',
                        required=False, action='store_true',
                        help='emit debug info')
    return parser.parse_args()


def run():
    args = parse_args()

    program: bytes
    with open(args.program[0], mode='r', encoding='utf-8') as hex_file:
        program = bytes.fromhex(' '.join([line.strip() for line in hex_file]))
    ram_size_mb: int = args.memory
    exec_type: ExecType = ExecType[args.exec_type]
    debug: bool = args.debug

    ctypes.cdll.LoadLibrary(VM_LIB).vm_run(program, len(program), ram_size_mb, exec_type, debug)


run()
