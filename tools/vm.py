from enum import IntEnum, unique


@unique
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

    def __repr__(self) -> str:
        return self.name


@unique
class RegImm(IntEnum):
    REG     =  0
    IMM     =  1

    def __repr__(self) -> str:
        return self.name


@unique
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

    def __repr__(self) -> str:
        return self.name
