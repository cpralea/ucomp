import argparse
import sys

from dataclasses import dataclass
from typing import Dict, List, TextIO, Tuple

from vm import Instruction, RegImm, Register


@dataclass
class VMInstrData:
    instr: Instruction
    ri: RegImm
    dst: Register | int | None  = None
    src: Register | int | None  = None
    len: int                    = 0


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


def unpack_opcode(hex_byte: str) -> Tuple[Instruction, RegImm]:
    instr: Instruction = Instruction((int(hex_byte, base=16) & ~0x01) >> 1)
    ri: RegImm = RegImm(int(hex_byte, base=16) & 0x01)
    return instr, ri


def load_hex_bytes(input: TextIO):
    if hex_bytes_buffer != []:
        return
    line: str = input.readline().strip()
    if line == '':
        return
    hex_bytes_buffer.extend(line.split(' '))


def peek_hex_byte(input: TextIO) -> str:
    if hex_bytes_buffer == []:
        load_hex_bytes(input)
    if hex_bytes_buffer == []:
        return ''
    return hex_bytes_buffer[0]


def peek_opcode(input: TextIO) -> Tuple[Instruction, RegImm] | None:
    hex_byte: str = peek_hex_byte(input)
    if not hex_byte:
        return None
    return unpack_opcode(hex_byte)


def peek_instr(input: TextIO) -> Instruction | None:
    opcode: Tuple[Instruction, RegImm] | None = peek_opcode(input)
    if opcode is None:
        return None
    instr, _ = opcode
    return instr


def get_hex_byte(input: TextIO) -> str:
    hex_byte: str = peek_hex_byte(input)
    if hex_byte:
        hex_bytes_buffer.pop(0)
    return hex_byte


def disasm_opcode(input: TextIO) -> Tuple[Instruction, RegImm]:
    return unpack_opcode(get_hex_byte(input))


def disasm_reg_reg(input: TextIO) -> Tuple[Register, Register]:
    rr: int = int(get_hex_byte(input), base=16)
    return Register(rr >> 4), Register(rr & 0x0f)


def disasm_imm(input: TextIO) -> int:
    hex_bytes: List[str] = []
    for _ in range(4):
        hex_bytes.append(get_hex_byte(input))
    return int(''.join(hex_bytes), base=16)


def disasm_instr(input: TextIO) -> VMInstrData:
    instr, ri = disasm_opcode(input)
    return VMInstrData(instr, ri, len=1)


def disasm_instr_r(input: TextIO) -> VMInstrData:
    instr, ri = disasm_opcode(input)
    dst, _ = disasm_reg_reg(input)
    return VMInstrData(instr, ri, dst=dst, len=2)


def disasm_instr_i(input: TextIO) -> VMInstrData:
    instr, ri = disasm_opcode(input)
    return VMInstrData(instr, ri, dst=disasm_imm(input), len=5)


def disasm_instr_rr(input: TextIO) -> VMInstrData:
    instr, ri = disasm_opcode(input)
    dst, src = disasm_reg_reg(input)
    return VMInstrData(instr, ri, dst=dst, src=src, len=2)


def disasm_instr_ri(input: TextIO) -> VMInstrData:
    instr, ri = disasm_opcode(input)
    dst, _ = disasm_reg_reg(input)
    return VMInstrData(instr, ri, dst=dst, src=disasm_imm(input), len=6)


def disasm_instr_src_dst(input: TextIO) -> VMInstrData:
    opcode: Tuple[Instruction, RegImm] | None = peek_opcode(input)
    assert opcode is not None
    _, ri = opcode
    match ri:
        case RegImm.REG:
            return disasm_instr_rr(input)
        case RegImm.IMM:
            return disasm_instr_ri(input)


def disasm_load(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_store(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_mov(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_add(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_sub(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_and(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_or(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_xor(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_not(input: TextIO) -> VMInstrData:
    return disasm_instr_r(input)
def disasm_cmp(input: TextIO) -> VMInstrData:
    return disasm_instr_src_dst(input)
def disasm_push(input: TextIO) -> VMInstrData:
    return disasm_instr_r(input)
def disasm_pop(input: TextIO) -> VMInstrData:
    return disasm_instr_r(input)
def disasm_call(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_ret(input: TextIO) -> VMInstrData:
    return disasm_instr(input)
def disasm_jmp(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_jmpz(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_jmpnz(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_jmpeq(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_jmpne(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_jmpgt(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_jmplt(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_jmpge(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_jmple(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)
def disasm_invoke(input: TextIO) -> VMInstrData:
    return disasm_instr_i(input)


def disasm_instruction(input: TextIO) -> VMInstrData | None:
    instr: Instruction | None = peek_instr(input)
    if instr is None:
        return None
    match instr:
        case Instruction.LOAD:
            return disasm_load(input)
        case Instruction.STORE:
            return disasm_store(input)
        case Instruction.MOV:
            return disasm_mov(input)
        case Instruction.ADD:
            return disasm_add(input)
        case Instruction.SUB:
            return disasm_sub(input)
        case Instruction.AND:
            return disasm_and(input)
        case Instruction.OR:
            return disasm_or(input)
        case Instruction.XOR:
            return disasm_xor(input)
        case Instruction.NOT:
            return disasm_not(input)
        case Instruction.CMP:
            return disasm_cmp(input)
        case Instruction.PUSH:
            return disasm_push(input)
        case Instruction.POP:
            return disasm_pop(input)
        case Instruction.CALL:
            return disasm_call(input)
        case Instruction.RET:
            return disasm_ret(input)
        case Instruction.JMP:
            return disasm_jmp(input)
        case Instruction.JMPZ:
            return disasm_jmpz(input)
        case Instruction.JMPNZ:
            return disasm_jmpnz(input)
        case Instruction.JMPEQ:
            return disasm_jmpeq(input)
        case Instruction.JMPNE:
            return disasm_jmpne(input)
        case Instruction.JMPGT:
            return disasm_jmpgt(input)
        case Instruction.JMPLT:
            return disasm_jmplt(input)
        case Instruction.JMPGE:
            return disasm_jmpge(input)
        case Instruction.JMPLE:
            return disasm_jmple(input)
        case Instruction.INVOKE:
            return disasm_invoke(input)
        case _:
            sys.exit(f"Instruction '{instr}' not supported yet.")


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
