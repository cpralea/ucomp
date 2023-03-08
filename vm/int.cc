#include <cstdlib>
#include <cstring>

#include "exe.h"


#define DISPATCH(OFFSET) { \
    reg[PC] += OFFSET; \
    goto *instr_exec_handle[instr(mem[reg[PC]])]; \
}

#define TRACE() if (debug) { trace(ri, dst, src, iv); }


Interpreter::Interpreter(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
: ExecutionEngine(prog, prog_size, ram_size_mb, debug)
{
    DBG("\ttype 'interpreter'" << endl);
}


void Interpreter::init_execution()
{
    DBG("Initializing memory ..." << endl);
    mem = std::unique_ptr<uint8_t[]>(new uint8_t[ram_size]);
    DBG("\tMemory @" << (void*) mem.get() << "[" << HEX(0, ram_size) << "]" << endl);

    DBG("Initializing registers ..." << endl);
    std::memset(&reg, 0, sizeof reg);
    reg[SP] = ram_size;
    reg[PC] = 5;
}


void Interpreter::load_program()
{
    DBG("Loading program ..." << endl);
    std::memmove(mem.get(), prog, prog_size);
}


void Interpreter::exec_program()
{
    DBG("Running program ..." << endl);

    static void* instr_exec_handle[] = {
        nullptr,
        &&_load,
        &&_store,
        &&_mov,
        &&_add,
        &&_sub,
        &&_and,
        &&_or,
        &&_xor,
        &&_not,
        &&_cmp,
        &&_push,
        &&_pop,
        &&_call,
        &&_ret,
        &&_jmp,
        &&_jmpz,
        &&_jmpnz,
        &&_jmpeq,
        &&_jmpne,
        &&_jmpgt,
        &&_jmplt,
        &&_jmpge,
        &&_jmple,
    };

    uint8_t ri, dst, src;
    uint32_t iv;

    DISPATCH(+0);

    _load: {
        dst = reg_dst(mem[reg[PC] + 1]);
        src = reg_src(mem[reg[PC] + 1]);
        TRACE();
        reg[dst] = uint8_to_uint32(mem[reg[src]]);
        DISPATCH(+2);
    }

    _store: {
        dst = reg_dst(mem[reg[PC] + 1]);
        src = reg_src(mem[reg[PC] + 1]);
        TRACE();
        uint8_to_uint32(mem[reg[dst]]) = reg[src];
        DISPATCH(+2);
    }

    _mov: {
        ri = reg_imm(mem[reg[PC]]);
        dst = reg_dst(mem[reg[PC] + 1]);
        switch (ri) {
        case REG:
            src = reg_src(mem[reg[PC] + 1]);
            TRACE();
            reg[dst] = reg[src];
            DISPATCH(+2);
        case IMM:
            iv = imm_val(mem[reg[PC] + 2]);
            TRACE();
            reg[dst] = iv;
            DISPATCH(+6);
        }
    }

    _add: {
        ri = reg_imm(mem[reg[PC]]);
        dst = reg_dst(mem[reg[PC] + 1]);
        switch (ri) {
        case REG:
            src = reg_src(mem[reg[PC] + 1]);
            TRACE();
            uint32_to_int32(reg[dst]) += uint32_to_int32(reg[src]);
            DISPATCH(+2);
        case IMM:
            iv = imm_val(mem[reg[PC] + 2]);
            TRACE();
            reg[dst] += iv;
            DISPATCH(+6);
        }
    }

    _sub: {
        ri = reg_imm(mem[reg[PC]]);
        dst = reg_dst(mem[reg[PC] + 1]);
        switch (ri) {
        case REG:
            src = reg_src(mem[reg[PC] + 1]);
            TRACE();
            uint32_to_int32(reg[dst]) -= uint32_to_int32(reg[src]);
            DISPATCH(+2);
        case IMM:
            iv = imm_val(mem[reg[PC] + 2]);
            TRACE();
            reg[dst] -= iv;
            DISPATCH(+6);
        }
    }

    _and: {
        ri = reg_imm(mem[reg[PC]]);
        dst = reg_dst(mem[reg[PC] + 1]);
        switch (ri) {
        case REG:
            src = reg_src(mem[reg[PC] + 1]);
            TRACE();
            reg[dst] &= reg[src];
            DISPATCH(+2);
        case IMM:
            iv = imm_val(mem[reg[PC] + 2]);
            TRACE();
            reg[dst] &= iv;
            DISPATCH(+6);
        }
    }

    _or: {
        ri = reg_imm(mem[reg[PC]]);
        dst = reg_dst(mem[reg[PC] + 1]);
        switch (ri) {
        case REG:
            src = reg_src(mem[reg[PC] + 1]);
            TRACE();
            reg[dst] |= reg[src];
            DISPATCH(+2);
        case IMM:
            iv = imm_val(mem[reg[PC] + 2]);
            TRACE();
            reg[dst] |= iv;
            DISPATCH(+6);
        }
    }

    _xor: {
        ri = reg_imm(mem[reg[PC]]);
        dst = reg_dst(mem[reg[PC] + 1]);
        switch (ri) {
        case REG:
            src = reg_src(mem[reg[PC] + 1]);
            TRACE();
            reg[dst] ^= reg[src];
            DISPATCH(+2);
        case IMM:
            iv = imm_val(mem[reg[PC] + 2]);
            TRACE();
            reg[dst] ^= iv;
            DISPATCH(+6);
        }
    }

    _not: {
        dst = reg_dst(mem[reg[PC] + 1]);
        TRACE();
        reg[dst] = ~reg[dst];
        DISPATCH(+2);
    }

    _cmp: {
        ri = reg_imm(mem[reg[PC]]);
        dst = reg_dst(mem[reg[PC] + 1]);
        switch (ri) {
        case REG:
            src = reg_src(mem[reg[PC] + 1]);
            TRACE();
            reg[FLAGS] = 0;
            if (reg[dst] == 0)
                reg[FLAGS] |= FLAG_Z;
            if (reg[dst] < reg[src])
                reg[FLAGS] |= FLAG_LT;
            else if (reg[dst] > reg[src])
                reg[FLAGS] |= FLAG_GT;
            else
                reg[FLAGS] |= FLAG_EQ;
            DISPATCH(+2);
        case IMM:
            iv = imm_val(mem[reg[PC] + 2]);
            TRACE();
            reg[FLAGS] = 0;
            if (reg[dst] == 0)
                reg[FLAGS] |= FLAG_Z;
            if (reg[dst] < iv)
                reg[FLAGS] |= FLAG_LT;
            else if (reg[dst] > iv)
                reg[FLAGS] |= FLAG_GT;
            else
                reg[FLAGS] |= FLAG_EQ;
            DISPATCH(+6);
        }
    }

    _push: {
        dst = reg_dst(mem[reg[PC] + 1]);
        TRACE();
        reg[SP] -= 4;
        uint8_to_uint32(mem[reg[SP]]) = reg[dst];
        DISPATCH(+2);
    }

    _pop: {
        dst = reg_dst(mem[reg[PC] + 1]);
        TRACE();
        reg[dst] = uint8_to_uint32(mem[reg[SP]]);
        reg[SP] += 4;
        DISPATCH(+2);
    }

    _call: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        reg[SP] -= 4;
        uint8_to_uint32(mem[reg[SP]]) = reg[PC] + 5;
        reg[PC] = iv;
        DISPATCH(+0);
    }

    _ret: {
        TRACE();
        reg[PC] = uint8_to_uint32(mem[reg[SP]]);
        reg[SP] += 4;
        DISPATCH(+0);
    }

    _jmp: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        switch (reg[PC]) {
        case SYS_ENTER_ADDR: {
            uint32_t syscall_id = imm_val(mem[reg[SP] + 4]);
            switch (syscall_id) {
            case SYSCALL_VM_EXIT:
                return;
            default:
                sys_enter();
                goto _ret;
            }
        }
        default:
            reg[PC] = iv;
            DISPATCH(+0);
        }
    }

    _jmpz: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        if (reg[FLAGS] & FLAG_Z) {
            reg[PC] = iv;
            DISPATCH(+0);
        } else {
            DISPATCH(+5);
        }
    }

    _jmpnz: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        if (reg[FLAGS] & FLAG_Z) {
            DISPATCH(+5);
        } else {
            reg[PC] = iv;
            DISPATCH(+0);
        }
    }

    _jmpeq: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        if (reg[FLAGS] & FLAG_EQ) {
            reg[PC] = iv;
            DISPATCH(+0);
        } else {
            DISPATCH(+5);
        }
    }

    _jmpne: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        if (reg[FLAGS] & FLAG_EQ) {
            DISPATCH(+5);
        } else {
            reg[PC] = iv;
            DISPATCH(+0);
        }
    }

    _jmpgt: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        if (reg[FLAGS] & FLAG_GT) {
            reg[PC] = iv;
            DISPATCH(+0);
        } else {
            DISPATCH(+5);
        }
    }

    _jmplt: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        if (reg[FLAGS] & FLAG_LT) {
            reg[PC] = iv;
            DISPATCH(+0);
        } else {
            DISPATCH(+5);
        }
    }

    _jmpge: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        if (reg[FLAGS] & (FLAG_GT | FLAG_EQ)) {
            reg[PC] = iv;
            DISPATCH(+0);
        } else {
            DISPATCH(+5);
        }
    }

    _jmple: {
        iv = imm_val(mem[reg[PC] + 1]);
        TRACE();
        if (reg[FLAGS] & (FLAG_LT | FLAG_EQ)) {
            reg[PC] = iv;
            DISPATCH(+0);
        } else {
            DISPATCH(+5);
        }
    }

    std::abort();
}


void Interpreter::fini_execution()
{
    dump_registers();
}


void Interpreter::sys_enter()
{
    uint32_t syscall_id = imm_val(mem[reg[SP] + 4]);
    switch (syscall_id) {
    case SYSCALL_VM_EXIT:
        std::abort();
    case SYSCALL_DISPLAY_INT: {
        int32_t val = imm_val(mem[reg[SP] + 8]);
        cout << val << endl;
        break;
    }
    default:
        std::abort();
    }
}


void Interpreter::trace(uint8_t ri, uint8_t dst, uint8_t src, uint32_t iv) const
{
    if (!debug)
        return;

    static const char* const R[] = {
        "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "flags", "sp", "pc"
    };
    auto HEX_DUMP = [this](uint8_t num_bytes) {
        uint8_t* addr = &mem[reg[PC]];
        for (uint8_t i = 0; i < num_bytes; i++)
            DBG_(HEX_(2, ((int) *(addr + i))) << " ");
        for (uint8_t i = 0; i < 6 - num_bytes; i++)
            DBG_("   ");
        DBG_("   ");
    };

    DBG("\t" << HEX(8, reg[PC]) << "   ");
    switch (instr(mem[reg[PC]])) {
    case LOAD:
        HEX_DUMP(2);      DBG_("load " << R[dst] << ", [" << R[src] << "]");                  break;
    case STORE:
        HEX_DUMP(2);      DBG_("store [" << R[dst] << "], " << R[src]);                       break;
    case MOV:
        HEX_DUMP(ri?6:2); DBG_("mov " << R[dst] << ", "); if (ri) DBG_(iv) else DBG_(R[src]); break;
    case ADD:
        HEX_DUMP(ri?6:2); DBG_("add " << R[dst] << ", "); if (ri) DBG_(iv) else DBG_(R[src]); break;
    case SUB:
        HEX_DUMP(ri?6:2); DBG_("sub " << R[dst] << ", "); if (ri) DBG_(iv) else DBG_(R[src]); break;
    case AND:
        HEX_DUMP(ri?6:2); DBG_("and " << R[dst] << ", "); if (ri) DBG_(iv) else DBG_(R[src]); break;
    case OR:
        HEX_DUMP(ri?6:2); DBG_("or " << R[dst] << ", "); if (ri) DBG_(iv) else DBG_(R[src]);  break;
    case XOR:
        HEX_DUMP(ri?6:2); DBG_("xor " << R[dst] << ", "); if (ri) DBG_(iv) else DBG_(R[src]); break;
    case NOT:
        HEX_DUMP(2);      DBG_("not " << R[dst]);                                             break;
    case CMP:
        HEX_DUMP(ri?6:2); DBG_("cmp " << R[dst] << ", "); if (ri) DBG_(iv) else DBG_(R[src]); break;
    case PUSH:
        HEX_DUMP(2);      DBG_("push " << R[dst]);                                            break;
    case POP:
        HEX_DUMP(2);      DBG_("pop " << R[dst]);                                             break;
    case CALL:
        HEX_DUMP(5);      DBG_("call " << HEX(8, iv));                                        break;
    case RET:
        HEX_DUMP(1);      DBG_("ret");                                                        break;
    case JMP:
        HEX_DUMP(5);      DBG_("jmp " << HEX(8, iv));                                         break;
    case JMPZ:
        HEX_DUMP(5);      DBG_("jmpz " << HEX(8, iv));                                        break;
    case JMPNZ:
        HEX_DUMP(5);      DBG_("jmpnz " << HEX(8, iv));                                       break;
    case JMPEQ:
        HEX_DUMP(5);      DBG_("jmpeq " << HEX(8, iv));                                       break;
    case JMPNE:
        HEX_DUMP(5);      DBG_("jmpne " << HEX(8, iv));                                       break;
    case JMPGT:
        HEX_DUMP(5);      DBG_("jmpgt " << HEX(8, iv));                                       break;
    case JMPLT:
        HEX_DUMP(5);      DBG_("jmplt " << HEX(8, iv));                                       break;
    case JMPGE:
        HEX_DUMP(5);      DBG_("jmpge " << HEX(8, iv));                                       break;
    case JMPLE:
        HEX_DUMP(5);      DBG_("jmple " << HEX(8, iv));                                       break;
    default:
        std::abort();
    }
    DBG_(endl);
}
