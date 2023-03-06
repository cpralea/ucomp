#include <cstdlib>
#include <cstring>

#include "exe.h"


#define DISPATCH(OFFSET) { \
    reg[PC] += OFFSET; \
    goto *instr_exec_handle[opcode(ram[reg[PC]])]; \
}


Interpreter::Interpreter(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
: ExecutionEngine(prog, prog_size, ram_size_mb, debug)
{
    DEBUG("\ttype 'interpreter'" << endl);
}


void Interpreter::init_execution()
{
    DEBUG("Initializing RAM ..." << endl);
    ram = std::unique_ptr<uint8_t[]>(new uint8_t[ram_size]);
    DEBUG("\tRAM @" << (void*) ram.get() << "[" << HEX(0, ram_size) << "]" << endl);

    DEBUG("Initializing registers ..." << endl);
    std::memset(&reg, 0, sizeof reg);
    reg[SP] = ram_size;
    reg[PC] = 5;
}


void Interpreter::load_program()
{
    DEBUG("Loading program ..." << endl);
    std::memmove(ram.get(), prog, prog_size);
}


void Interpreter::exec_program()
{
    DEBUG("Running program ..." << endl);

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

    DISPATCH(+0);
    _load: {
        std::abort();
    }
    _store: {
        std::abort();
    }
    _mov: {
        ri = reg_imm(ram[reg[PC]]);
        dst = reg_dst(ram[reg[PC]+1]);
        switch (ri) {
        case REG:
            src = reg_src(ram[reg[PC]+1]);
            reg[dst] = reg[src];
            DISPATCH(+2);
        case IMM:
            reg[dst] = imm(&ram[reg[PC]+2]);
            DISPATCH(+6);
        }
    }
    _add: {
        std::abort();
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
        dump_registers();
        std::abort();
    }
    _pop: {
        std::abort();
    }
    _call: {
        std::abort();
    }
    _ret: {
        std::abort();
    }
    _jmp: {
        std::abort();
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
}


void Interpreter::fini_execution()
{
    dump_registers();
}
