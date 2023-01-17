from enum import IntEnum


class Operation(IntEnum):
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
    R14     = 14
    SP      = 15


def gen_opcode(op: Operation, ri: RegImm) -> int:
    return (op << 1) + ri
def gen_op(op: Operation) -> int:
    return gen_opcode(op, RegImm.REG)
def gen_rr(dst: Register, src: Register) -> int:
    return (dst << 4) + src
def gen_ri(reg: Register, imm: int) -> int:
    return ((reg << 4) << 32) + imm
def gen_op_rr(op: Operation, dst: Register, src: Register) -> int:
    return (gen_opcode(op, RegImm.REG) << 8) + gen_rr(dst, src)
def gen_op_ri(op: Operation, dst: Register, src: int) -> int:
    return (gen_opcode(op, RegImm.IMM) << 40) + gen_ri(dst, src)
def gen_r(reg: Register) -> int:
    return reg << 4
def gen_i(imm: int) -> int:
    return imm
def gen_op_r(op: Operation, reg: Register) -> int:
    return (gen_opcode(op, RegImm.REG) << 8) + gen_r(reg)
def gen_op_i(op: Operation, imm: int) -> int:
    return (gen_opcode(op, RegImm.IMM) << 32) + gen_i(imm)


def gen_load_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.LOAD, dst, src)
def gen_store_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.STORE, dst, src)
def gen_mov_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.MOV, dst, src)
def gen_mov_ri(dst: Register, src: int) -> int:
    return gen_op_ri(Operation.MOV, dst, src)
def gen_add_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.ADD, dst, src)
def gen_add_ri(dst: Register, src: int) -> int:
    return gen_op_ri(Operation.ADD, dst, src)
def gen_sub_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.SUB, dst, src)
def gen_sub_ri(dst: Register, src: int) -> int:
    return gen_op_ri(Operation.SUB, dst, src)
def gen_and_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.AND, dst, src)
def gen_and_ri(dst: Register, src: int) -> int:
    return gen_op_ri(Operation.AND, dst, src)
def gen_or_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.OR, dst, src)
def gen_or_ri(dst: Register, src: int) -> int:
    return gen_op_ri(Operation.OR, dst, src)
def gen_xor_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.XOR, dst, src)
def gen_xor_ri(dst: Register, src: int) -> int:
    return gen_op_ri(Operation.XOR, dst, src)
def gen_not_r(reg: Register) -> int:
    return gen_op_r(Operation.NOT, reg)
def gen_cmp_rr(dst: Register, src: Register) -> int:
    return gen_op_rr(Operation.CMP, dst, src)
def gen_cmp_ri(dst: Register, src: int) -> int:
    return gen_op_ri(Operation.CMP, dst, src)
def gen_push_r(reg: Register) -> int:
    return gen_op_r(Operation.PUSH, reg)
def gen_pop_r(reg: Register) -> int:
    return gen_op_r(Operation.POP, reg)
def gen_jmp_i(imm: int) -> int:
    return gen_op_i(Operation.JMP, imm)
def gen_jmpz_i(imm: int) -> int:
    return gen_op_i(Operation.JMPZ, imm)
def gen_jmpnz_i(imm: int) -> int:
    return gen_op_i(Operation.JMPNZ, imm)
def gen_jmpeq_i(imm: int) -> int:
    return gen_op_i(Operation.JMPEQ, imm)
def gen_jmpne_i(imm: int) -> int:
    return gen_op_i(Operation.JMPNE, imm)
def gen_jmpgt_i(imm: int) -> int:
    return gen_op_i(Operation.JMPGT, imm)
def gen_jmplt_i(imm: int) -> int:
    return gen_op_i(Operation.JMPLT, imm)
def gen_jmpge_i(imm: int) -> int:
    return gen_op_i(Operation.JMPGE, imm)
def gen_jmple_i(imm: int) -> int:
    return gen_op_i(Operation.JMPLE, imm)
def gen_call_i(imm: int) -> int:
    return gen_op_i(Operation.CALL, imm)
def gen_ret() -> int:
    return gen_op(Operation.RET)
def gen_invoke_i(imm: int) -> int:
    return gen_op_i(Operation.INVOKE, imm)
