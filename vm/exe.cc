#include "exe.h"


ExecutionEngine::ExecutionEngine(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
: prog(prog), prog_size(prog_size), ram_size(ram_size_mb << 20), debug(debug)
, ram(nullptr)
{
    DEBUG("Initializing VM with:" << endl);
    DEBUG("\tprogram at " << prog << ", size " << prog_size << endl);
    DEBUG("\tmemory " << ram_size_mb << " MiB" << endl);
}


ExecutionEngine::~ExecutionEngine()
{
}


void ExecutionEngine::dump_registers() const
{
    DEBUG("Registers:" << endl);
    DEBUG("\tR0    = " << HEX(8, reg[R0])    << endl);
    DEBUG("\tR1    = " << HEX(8, reg[R1])    << endl);
    DEBUG("\tR2    = " << HEX(8, reg[R2])    << endl);
    DEBUG("\tR3    = " << HEX(8, reg[R3])    << endl);
    DEBUG("\tR4    = " << HEX(8, reg[R4])    << endl);
    DEBUG("\tR5    = " << HEX(8, reg[R5])    << endl);
    DEBUG("\tR6    = " << HEX(8, reg[R6])    << endl);
    DEBUG("\tR7    = " << HEX(8, reg[R7])    << endl);
    DEBUG("\tR8    = " << HEX(8, reg[R8])    << endl);
    DEBUG("\tR9    = " << HEX(8, reg[R9])    << endl);
    DEBUG("\tR10   = " << HEX(8, reg[R10])   << endl);
    DEBUG("\tR11   = " << HEX(8, reg[R11])   << endl);
    DEBUG("\tR12   = " << HEX(8, reg[R12])   << endl);
    DEBUG("\tFLAGS = " << HEX(8, reg[FLAGS]) << endl);
    DEBUG("\tSP    = " << HEX(8, reg[SP])    << endl);
    DEBUG("\tPC    = " << HEX(8, reg[PC])    << endl);
}
