#include <cstring>

#include "exe.h"


Interpreter::Interpreter(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
: ExecutionEngine(prog, prog_size, ram_size_mb, debug)
, ram(nullptr)
{
    DEBUG("\ttype 'interpreter'" << endl);
}


void Interpreter::init()
{
    DEBUG("Initializing RAM ..." << endl);
    ram.reset(new uint8_t[ram_size]);
    DEBUG("\tRAM @0x" << HEX(16) << (uint64_t) ram.get() << "[0x" << HEX(8) << ram_size << "]" << endl);

    DEBUG("Initializing registers ..." << endl);
    std::memset(&register_file, 0, sizeof register_file);
    register_file.PC = 5;
}


void Interpreter::load()
{
    DEBUG("Loading program ..." << endl);
    std::memmove(ram.get(), prog, prog_size);
}


void Interpreter::run()
{
    DEBUG("Running program ..." << endl);
}


void Interpreter::fini()
{
    dump_registers();
}
