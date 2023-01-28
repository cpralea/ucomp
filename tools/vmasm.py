import re
import sys

from enum import IntEnum
from typing import Callable, Dict, List, Optional, TextIO


class Instruction(IntEnum):
    LOAD    =  1
    STORE   =  2
    MOV     =  3
    ADD     =  4
    SUB     =  5
    AND     =  6
    OR      =  7
    XOR     =  8
    NOT     =  9
    CMP     = 10
    PUSH    = 11
    POP     = 12
    CALL    = 13
    RET     = 14
    JMP     = 15
    JMPZ    = 16
    JMPNZ   = 17
    JMPEQ   = 18
    JMPNE   = 19
    JMPGT   = 20
    JMPLT   = 21
    JMPGE   = 22
    JMPLE   = 23
    INVOKE  = 24


class RegImm(IntEnum):
    REG     =  0
    IMM     =  1


class Register(IntEnum):
    R0      =  0
    R1      =  1
    R2      =  2
    R3      =  3
    R4      =  4
    R5      =  5
    R6      =  6
    R7      =  7
    R8      =  8
    R9      =  9
    R10     = 10
    R11     = 11
    R12     = 12
    R13     = 13
    SP      = 14
    PC      = 15


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

labelCurTopLevel: str = 'entry'
labelRefs: Dict[str, List[int]] = {}
labelAddr: Dict[str, int] = {
    "$vm_exit" : 0xffffff00 | 0
}

program: List[int] = []


def is_high_level_label(label: str) -> bool:
    return not label.startswith(low_level_label_start)
def is_low_level_label(label: str) -> bool:
    return not is_high_level_label(label)
def is_sys_level_label(label: str) -> bool:
    return label.startswith(sys_level_label_start)


def mangle_label(label: str) -> str:
    return label if is_high_level_label(label) else f"{labelCurTopLevel}{label}"


def gen_opcode(instr: Instruction, ri: RegImm) -> int:
    return (instr << 1) + ri
def gen_instr(instr: Instruction) -> int:
    return gen_opcode(instr, RegImm.REG)
def gen_rr(dst: Register, src: Register) -> int:
    return (dst << 4) + src
def gen_ri(reg: Register, imm: int) -> int:
    return ((reg << 4) << 32) + imm
def gen_instr_rr(instr: Instruction, dst: Register, src: Register) -> int:
    return (gen_opcode(instr, RegImm.REG) << 8) + gen_rr(dst, src)
def gen_instr_ri(instr: Instruction, dst: Register, src: int) -> int:
    return (gen_opcode(instr, RegImm.IMM) << 40) + gen_ri(dst, src)
def gen_r(reg: Register) -> int:
    return reg << 4
def gen_i(imm: int) -> int:
    return imm
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
def gen_call_i(imm: int) -> int:
    return gen_instr_i(Instruction.CALL, imm)
def gen_ret() -> int:
    return gen_instr(Instruction.RET)
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
    if label not in labelRefs:
        labelRefs[label] = []
    labelRefs[label].append(len(program))

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


def asm_instr(instr: str, line: str):
    match instr.upper():
        case 'LOAD':
            program.append(asm_load(line))
        case 'STORE':
            program.append(asm_store(line))
        case 'MOV':
            program.append(asm_mov(line))
        case 'ADD':
            program.append(asm_add(line))
        case 'SUB':
            program.append(asm_sub(line))
        case 'AND':
            program.append(asm_and(line))
        case 'OR':
            program.append(asm_or(line))
        case 'XOR':
            program.append(asm_xor(line))
        case 'NOT':
            program.append(asm_not(line))
        case 'CMP':
            program.append(asm_cmp(line))
        case 'PUSH':
            program.append(asm_push(line))
        case 'POP':
            program.append(asm_pop(line))
        case 'CALL':
            program.append(asm_call(line))
        case 'RET':
            program.append(asm_ret(line))
        case 'JMP':
            program.append(asm_jmp(line))
        case 'JMPZ':
            program.append(asm_jmpz(line))
        case 'JMPNZ':
            program.append(asm_jmpnz(line))
        case 'JMPEQ':
            program.append(asm_jmpeq(line))
        case 'JMPNE':
            program.append(asm_jmpne(line))
        case 'JMPGT':
            program.append(asm_jmpgt(line))
        case 'JMPLT':
            program.append(asm_jmplt(line))
        case 'JMPGE':
            program.append(asm_jmpge(line))
        case 'JMPLE':
            program.append(asm_jmple(line))
        case 'INVOKE':
            program.append(asm_invoke(line))
        case _:
            sys.exit(f"Unknown instruction '{instr}'.")


def asm_label(label: str):
    global labelCurTopLevel
    if is_high_level_label(label):
        labelCurTopLevel = label
    labelAddr[mangle_label(label)] = len(program)


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
    if len(line) == 0:
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
    print(labelAddr)
    for label, refs in labelRefs.items():
        addr = labelAddr[label]
        for ref in refs:
            program[ref] = program[ref] | addr


def asm_file(file: TextIO):
    for line in file:
        asm_line(line)
    link()


def dump_program():
    for idx, instr in enumerate(program):
        print(f"{idx:04}   0x{instr:012x}")


asm_file(sys.stdin)
dump_program()
