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
        reg[dst] = mem[reg[src]];
        DISPATCH(+2);
    }

    _store: {
        std::abort();
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
            iv = imm_val(&mem[reg[PC] + 2]);
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
            as_int32_t(reg[dst]) += as_int32_t(reg[src]);
            DISPATCH(+2);
        case IMM:
            iv = imm_val(&mem[reg[PC] + 2]);
            TRACE();
            reg[dst] += iv;
            DISPATCH(+6);
        }
    }

    _sub: {
        std::abort();
    }

    _and: {
        std::abort();
    }

    _or: {
        std::abort();
    }

    _xor: {
        std::abort();
    }

    _not: {
        std::abort();
    }

    _cmp: {
        std::abort();
    }

    _push: {
        dst = reg_dst(mem[reg[PC] + 1]);
        TRACE();
        reg[SP] -= 4;
        mem[reg[SP]] = reg[dst];
        DISPATCH(+2);
    }

    _pop: {
        dst = reg_dst(mem[reg[PC] + 1]);
        TRACE();
        reg[dst] = mem[reg[SP]];
        reg[SP] += 4;
        DISPATCH(+2);
    }

    _call: {
        iv = imm_val(&mem[reg[PC] + 1]);
        TRACE();
        reg[SP] -= 4;
        mem[reg[SP]] = reg[PC] + 5;
        reg[PC] = iv;
        DISPATCH(+0);
    }

    _ret: {
        TRACE();
        reg[PC] = mem[reg[SP]];
        reg[SP] += 4;
        DISPATCH(+0);
    }

    _jmp: {
        iv = imm_val(&mem[reg[PC] + 1]);
        TRACE();
        switch (reg[PC]) {
        case SYS_ENTER_ADDR: {
            uint32_t syscall_id = imm_val(&mem[reg[SP] + 4]);
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
        std::abort();
    }

    _jmpnz: {
        std::abort();
    }

    _jmpeq: {
        std::abort();
    }

    _jmpne: {
        std::abort();
    }

    _jmpgt: {
        std::abort();
    }

    _jmplt: {
        std::abort();
    }

    _jmpge: {
        std::abort();
    }

    _jmple: {
        std::abort();
    }

    std::abort();
}


void Interpreter::fini_execution()
{
    dump_registers();
}


void Interpreter::sys_enter()
{
}


void Interpreter::trace(uint8_t ri, uint8_t dst, uint8_t src, uint32_t iv) const
{
    static const char* const R[] = {
        "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "flags", "sp", "pc"
    };

    uint32_t addr = reg[PC];
    uint8_t opcode = mem[addr];
    uint8_t in = instr(opcode);

    DBG(HEX(8, addr) << "   ");

    switch (in) {
    case LOAD:
        DBG_("load " << R[dst] << ", [" << R[src] << "]" << endl);
        break;
    case STORE:
    case MOV:
        DBG_("mov " << R[dst] << ", ");
        if (ri == REG) { DBG_(R[src] << endl); } else { DBG_(iv << endl); }
        break;
    case ADD:
        DBG_("add " << R[dst] << ", ");
        if (ri == REG) { DBG_(R[src] << endl); } else { DBG_(iv << endl); }
        break;
    case SUB:
    case AND:
    case OR:
    case XOR:
    case NOT:
    case CMP:
    case PUSH:
        DBG_("push " << R[dst] << endl);
        break;
    case POP:
        DBG_("pop " << R[dst] << endl);
        break;
    case CALL:
        DBG_("call " << HEX(8, iv) << endl);
        break;
    case RET:
        DBG_("ret" << endl);
        break;
    case JMP:
        DBG_("jmp " << HEX(8, iv) << endl);
        break;
    case JMPZ:
    case JMPNZ:
    case JMPEQ:
    case JMPNE:
    case JMPGT:
    case JMPLT:
    case JMPGE:
    case JMPLE:
    default:
        std::abort();
    }
}
