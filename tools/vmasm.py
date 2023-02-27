import argparse
import re
import sys

from math import ceil
from typing import Callable, Dict, List, Optional, TextIO

from vm import Instruction, RegImm, Register


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='VM assembler.')
    parser.add_argument('input_file', metavar='ASM', type=str, nargs='?', \
                        help='input file to process; defaults to STDIN if unspecified')
    parser.add_argument('-o', '--output', metavar='HEX', type=str, dest='output_file', \
                        required=False, \
                        help='output file to emit VM code to; defaults to STDOUT if unspecified')
    parser.add_argument('-l', '--labels', metavar='LBL', type=str, dest='labels_file', \
                        required=False, \
                        help='output file to emit assembler labels to; defaults to none if unspecified')
    return parser.parse_args()


regex_imm_hex               = re.compile(r'^(0x[0-9a-fA-F]+)$')
regex_imm_dec               = re.compile(r'^([0-9]+)$')
regex_label                 = re.compile(r'^(.+):$')
regex_instr                 = re.compile(r'^([a-zA-Z]+).*$')
regex_load                  = re.compile(r'^LOAD\s+([^\s]+)\s*,\s*\[([^\s]+)\]$')
regex_store                 = re.compile(r'^STORE\s+\[([^\s]+)\]\s*,\s*([^\s]+)$')
regex_generic_instr_dst_src = re.compile(r'^[a-zA-Z]+\s+([^\s]+)\s*,\s*([^\s]+)$')
regex_generic_instr_op      = re.compile(r'^[a-zA-Z]+\s+([^\s]+)\s*$')

low_level_label_start: str = '.'
sys_level_label_start: str = '$'

label_cur_top_level: str = 'entry'
label_refs: Dict[str, List[int]] = {}
label_addr: Dict[str, int] = {
    "$vm_exit" : 0xffffff00 | 0
}

program: List[int] = []
program_size: int = 0


def is_high_level_label(label: str) -> bool:
    return not label.startswith(low_level_label_start)
def is_low_level_label(label: str) -> bool:
    return not is_high_level_label(label)
def is_sys_level_label(label: str) -> bool:
    return label.startswith(sys_level_label_start)


def mangle_label(label: str) -> str:
    return label if is_high_level_label(label) else f"{label_cur_top_level}:{label}"
def demangle_label(label: str) -> List[str]:
    return label.split(':')


def gen_i(imm: int) -> int:
    return imm
def gen_opcode(instr: Instruction, ri: RegImm) -> int:
    return (instr << 1) + ri
def gen_instr(instr: Instruction) -> int:
    return gen_opcode(instr, RegImm.REG)
def gen_rr(dst: Register, src: Register) -> int:
    return (dst << 4) + src
def gen_ri(reg: Register, imm: int) -> int:
    return ((reg << 4) << 32) + gen_i(imm)
def gen_instr_rr(instr: Instruction, dst: Register, src: Register) -> int:
    return (gen_opcode(instr, RegImm.REG) << 8) + gen_rr(dst, src)
def gen_instr_ri(instr: Instruction, dst: Register, src: int) -> int:
    return (gen_opcode(instr, RegImm.IMM) << 40) + gen_ri(dst, src)
def gen_r(reg: Register) -> int:
    return reg << 4
def gen_instr_r(instr: Instruction, reg: Register) -> int:
    return (gen_opcode(instr, RegImm.REG) << 8) + gen_r(reg)
def gen_instr_i(instr: Instruction, imm: int) -> int:
    return (gen_opcode(instr, RegImm.IMM) << 32) + gen_i(imm)


def gen_load_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.LOAD, dst, src)
def gen_store_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.STORE, dst, src)
def gen_mov_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.MOV, dst, src)
def gen_mov_ri(dst: Register, src: int) -> int:
    return gen_instr_ri(Instruction.MOV, dst, src)
def gen_add_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.ADD, dst, src)
def gen_add_ri(dst: Register, src: int) -> int:
    return gen_instr_ri(Instruction.ADD, dst, src)
def gen_sub_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.SUB, dst, src)
def gen_sub_ri(dst: Register, src: int) -> int:
    return gen_instr_ri(Instruction.SUB, dst, src)
def gen_and_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.AND, dst, src)
def gen_and_ri(dst: Register, src: int) -> int:
    return gen_instr_ri(Instruction.AND, dst, src)
def gen_or_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.OR, dst, src)
def gen_or_ri(dst: Register, src: int) -> int:
    return gen_instr_ri(Instruction.OR, dst, src)
def gen_xor_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.XOR, dst, src)
def gen_xor_ri(dst: Register, src: int) -> int:
    return gen_instr_ri(Instruction.XOR, dst, src)
def gen_not_r(reg: Register) -> int:
    return gen_instr_r(Instruction.NOT, reg)
def gen_cmp_rr(dst: Register, src: Register) -> int:
    return gen_instr_rr(Instruction.CMP, dst, src)
def gen_cmp_ri(dst: Register, src: int) -> int:
    return gen_instr_ri(Instruction.CMP, dst, src)
def gen_push_r(reg: Register) -> int:
    return gen_instr_r(Instruction.PUSH, reg)
def gen_pop_r(reg: Register) -> int:
    return gen_instr_r(Instruction.POP, reg)
def gen_call_i(imm: int) -> int:
    return gen_instr_i(Instruction.CALL, imm)
def gen_ret() -> int:
    return gen_instr(Instruction.RET)
def gen_jmp_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMP, imm)
def gen_jmpz_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMPZ, imm)
def gen_jmpnz_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMPNZ, imm)
def gen_jmpeq_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMPEQ, imm)
def gen_jmpne_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMPNE, imm)
def gen_jmpgt_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMPGT, imm)
def gen_jmplt_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMPLT, imm)
def gen_jmpge_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMPGE, imm)
def gen_jmple_i(imm: int) -> int:
    return gen_instr_i(Instruction.JMPLE, imm)
def gen_invoke_i(imm: int) -> int:
    return gen_instr_i(Instruction.INVOKE, imm)


def asm_generic_instr_dst_src(
        line: str,
        pattern: re.Pattern[str],
        gen_rr: Callable[[Register, Register], int],
        gen_ri: Callable[[Register, int], int]
    ) -> int:

    m = pattern.match(line.upper())
    assert m is not None

    dst, src = Register[m.group(1).upper()], m.group(2).upper()

    m = regex_imm_dec.match(src)
    if m is None:
        m = regex_imm_hex.match(src)
    if m is not None:
        src = int(src)
        return gen_ri(dst, src)

    src = Register[src]
    return gen_rr(dst, src)


def asm_generic_instr_op(
        line: str,
        pattern: re.Pattern[str],
        gen_r: Optional[Callable[[Register], int]],
        gen_i: Optional[Callable[[int], int]]
    ) -> int:

    m = pattern.match(line.upper())
    assert m is not None
    
    op = m.group(1).upper()
    
    m = regex_imm_dec.match(op)
    if m is None:
        m = regex_imm_hex.match(op)
    if m is not None:
        op = int(op)
        assert (gen_r is None) and (gen_i is not None)
        return gen_i(op)

    if op in dir(Register):
        op = Register[op]
        assert (gen_r is not None) and (gen_i is None)
        return gen_r(op)

    label = mangle_label(op.lower())
    if label not in label_refs:
        label_refs[label] = []
    label_refs[label].append(len(program))

    op = 0
    assert (gen_r is None) and (gen_i is not None)
    return gen_i(op)


def asm_load(line: str) -> int:
    m = regex_load.match(line.upper())
    assert m is not None
    dst, src = Register[m.group(1).upper()], Register[m.group(2).upper()]
    return gen_load_rr(dst, src)
def asm_store(line: str) -> int:
    m = regex_store.match(line.upper())
    assert m is not None
    dst, src = Register[m.group(1).upper()], Register[m.group(2).upper()]
    return gen_store_rr(dst, src)
def asm_mov(line: str) -> int:
    return asm_generic_instr_dst_src(line, regex_generic_instr_dst_src, gen_mov_rr, gen_mov_ri)
def asm_add(line: str) -> int:
    return asm_generic_instr_dst_src(line, regex_generic_instr_dst_src, gen_add_rr, gen_add_ri)
def asm_sub(line: str) -> int:
    return asm_generic_instr_dst_src(line, regex_generic_instr_dst_src, gen_sub_rr, gen_sub_ri)
def asm_and(line: str) -> int:
    return asm_generic_instr_dst_src(line, regex_generic_instr_dst_src, gen_and_rr, gen_and_ri)
def asm_or(line: str) -> int:
    return asm_generic_instr_dst_src(line, regex_generic_instr_dst_src, gen_or_rr, gen_or_ri)
def asm_xor(line: str) -> int:
    return asm_generic_instr_dst_src(line, regex_generic_instr_dst_src, gen_xor_rr, gen_xor_ri)
def asm_not(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, gen_not_r, None)
def asm_cmp(line: str) -> int:
    return asm_generic_instr_dst_src(line, regex_generic_instr_dst_src, gen_cmp_rr, gen_cmp_ri)
def asm_push(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, gen_push_r, None)
def asm_pop(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, gen_pop_r, None)
def asm_call(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_call_i)
def asm_ret(line: str) -> int:
    return gen_ret()
def asm_jmp(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmp_i)
def asm_jmpz(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmpz_i)
def asm_jmpnz(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmpnz_i)
def asm_jmpeq(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmpeq_i)
def asm_jmpne(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmpne_i)
def asm_jmpgt(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmpgt_i)
def asm_jmplt(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmplt_i)
def asm_jmpge(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmpge_i)
def asm_jmple(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_jmple_i)
def asm_invoke(line: str) -> int:
    return asm_generic_instr_op(line, regex_generic_instr_op, None, gen_invoke_i)


def num_bytes(bin_enc: int) -> int:
    return ceil(4 * len(f"{bin_enc:x}") / 8)


def asm_instr(instr: str, line: str):
    match instr.upper():
        case 'LOAD':
            bin_enc = asm_load(line)
        case 'STORE':
            bin_enc = asm_store(line)
        case 'MOV':
            bin_enc = asm_mov(line)
        case 'ADD':
            bin_enc = asm_add(line)
        case 'SUB':
            bin_enc = asm_sub(line)
        case 'AND':
            bin_enc = asm_and(line)
        case 'OR':
            bin_enc = asm_or(line)
        case 'XOR':
            bin_enc = asm_xor(line)
        case 'NOT':
            bin_enc = asm_not(line)
        case 'CMP':
            bin_enc = asm_cmp(line)
        case 'PUSH':
            bin_enc = asm_push(line)
        case 'POP':
            bin_enc = asm_pop(line)
        case 'CALL':
            bin_enc = asm_call(line)
        case 'RET':
            bin_enc = asm_ret(line)
        case 'JMP':
            bin_enc = asm_jmp(line)
        case 'JMPZ':
            bin_enc = asm_jmpz(line)
        case 'JMPNZ':
            bin_enc = asm_jmpnz(line)
        case 'JMPEQ':
            bin_enc = asm_jmpeq(line)
        case 'JMPNE':
            bin_enc = asm_jmpne(line)
        case 'JMPGT':
            bin_enc = asm_jmpgt(line)
        case 'JMPLT':
            bin_enc = asm_jmplt(line)
        case 'JMPGE':
            bin_enc = asm_jmpge(line)
        case 'JMPLE':
            bin_enc = asm_jmple(line)
        case 'INVOKE':
            bin_enc = asm_invoke(line)
        case _:
            sys.exit(f"Unknown instruction '{instr}'.")
    
    program.append(bin_enc)

    global program_size
    program_size += num_bytes(bin_enc)


def asm_label(label: str):
    global label_cur_top_level
    if is_high_level_label(label):
        label_cur_top_level = label
    label_addr[mangle_label(label)] = program_size


def strip_comment(line: str) -> str:
    pos = line.find(";")
    if pos != -1:
        line = line[:pos]
    return line


def strip_whitespaces(line: str) -> str:
    return line.strip()


def asm_line(line: str):
    line = strip_comment(line)
    line = strip_whitespaces(line)
    if not line:
        return

    m_label = regex_label.match(line)
    if m_label is not None:
        label = m_label.group(1)
        asm_label(label)
        return
    
    m_instr = regex_instr.match(line)
    if m_instr is not None:
        instr = m_instr.group(1)
        asm_instr(instr, line)
        return


def link():
    for label, refs in label_refs.items():
        addr = label_addr[label]
        for ref in refs:
            program[ref] |= addr


def asm_file(input: TextIO):
    for line in input:
        asm_line(line)
    link()


def dump_program(output: TextIO):
    for bin_enc in program:
        hex_enc = f"{bin_enc:x}"
        if len(hex_enc) % 2 == 1:
            hex_enc = '0' + hex_enc
        print(' '.join([hex_enc[i:i+2] for i in range(0, len(hex_enc), 2)]), file=output)


def assemble():
    args = parse_args()

    input_file: TextIO = sys.stdin
    output_file: TextIO = sys.stdout
    labels_file: TextIO | None = None

    if args.input_file is not None:
        input_file = open(args.input_file, mode='r', encoding='utf-8') # type: ignore
    if args.output_file is not None:
        output_file = open(args.output_file, mode='w', encoding='utf-8') # type: ignore
    if args.labels_file is not None:
        labels_file = open(args.labels_file, mode='w', encoding='utf-8') # type: ignore

    with output_file as output:
        with input_file as input:
            asm_file(input)
            dump_program(output)
        if labels_file is not None:
            with labels_file as labels:
                for addr, label in sorted([(a, demangle_label(l)[-1]) for (l, a) in label_addr.items()]):
                    print(f"{addr:>8x}   {label}", file=labels)


assemble()
