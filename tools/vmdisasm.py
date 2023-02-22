import argparse
import sys

from dataclasses import dataclass
from typing import Dict, List, TextIO

from vm import Instruction


@dataclass
class VMInstrData:
    instr: Instruction
    len: int


hex_bytes_buffer: List[str] = []

cur_addr: int = 0
program: Dict[int, VMInstrData] = {}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='VM disassembler.')
    parser.add_argument('input_file', metavar='INPUT', type=str, nargs='?', \
                        help='input file to process; defaults to STDIN if unspecified')
    parser.add_argument('-o', '--output', metavar='OUTPUT', type=str, dest='output_file', \
                        required=False, \
                        help='output file to emit; defaults to STDOUT if unspecified')
    return parser.parse_args()


def load_hex_bytes(input: TextIO):
    if hex_bytes_buffer != []:
        return
    line: str = input.readline().strip()
    if line == '':
        return
    hex_bytes_buffer.extend(line.split(' '))


def get_hex_byte(input: TextIO) -> str:
    if hex_bytes_buffer == []:
        load_hex_bytes(input)
    if hex_bytes_buffer == []:
        return ''
    return hex_bytes_buffer.pop()


def disasm_instruction(input: TextIO) -> VMInstrData | None:
    hex_byte: str = get_hex_byte(input)
    if not hex_byte:
        return None
    return VMInstrData(Instruction.RET, 1)


def disasm_file(input: TextIO):
    global cur_addr
    instr_data: VMInstrData | None = disasm_instruction(input)
    while instr_data is not None:
        program[cur_addr] = instr_data
        cur_addr += instr_data.len
        instr_data = disasm_instruction(input)


def dump_program(output: TextIO):
    from pprint import PrettyPrinter
    PrettyPrinter().pprint(program)


def disassemble():
    args = parse_args()

    input_file: TextIO = sys.stdin
    output_file: TextIO = sys.stdout

    if args.input_file is not None:
        input_file = open(args.input_file, mode='r', encoding='utf-8') # type: ignore
    if args.output_file is not None:
        output_file = open(args.output_file, mode='w', encoding='utf-8') # type: ignore

    with output_file as output:
        with input_file as input:
            disasm_file(input)
            dump_program(output)


disassemble()
