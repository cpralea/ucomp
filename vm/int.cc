#include <cstring>

#include "exec.h"


Interpreter::Interpreter(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
: ExecutionEngine(prog, prog_size, ram_size_mb, debug)
, ram(new uint8_t[ram_size])
{
    std::memmove(ram.get(), prog, prog_size);

    DEBUG("\ttype 'interpreter'" << endl);
    DEBUG(std::hex << std::showbase <<
        "RAM @" << static_cast<void*>(ram.get()) << "[" << ram_size << "]"
    << std::dec << endl);
}


void Interpreter::execute()
{
}
