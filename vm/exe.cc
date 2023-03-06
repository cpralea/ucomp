#include "exe.h"


ExecutionEngine::ExecutionEngine(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
: prog(prog), prog_size(prog_size), ram_size(ram_size_mb << 20), debug(debug)
, mem(nullptr)
{
    DBG("Initializing VM with:" << endl);
    DBG("\tprogram at " << prog << ", size " << prog_size << endl);
    DBG("\tmemory " << ram_size_mb << " MiB" << endl);
}


ExecutionEngine::~ExecutionEngine()
{
}


void ExecutionEngine::dump_registers() const
{
    DBG("Registers:" << endl);
    DBG("\tR0    = " << HEX(8, reg[R0])    << endl);
    DBG("\tR1    = " << HEX(8, reg[R1])    << endl);
    DBG("\tR2    = " << HEX(8, reg[R2])    << endl);
    DBG("\tR3    = " << HEX(8, reg[R3])    << endl);
    DBG("\tR4    = " << HEX(8, reg[R4])    << endl);
    DBG("\tR5    = " << HEX(8, reg[R5])    << endl);
    DBG("\tR6    = " << HEX(8, reg[R6])    << endl);
    DBG("\tR7    = " << HEX(8, reg[R7])    << endl);
    DBG("\tR8    = " << HEX(8, reg[R8])    << endl);
    DBG("\tR9    = " << HEX(8, reg[R9])    << endl);
    DBG("\tR10   = " << HEX(8, reg[R10])   << endl);
    DBG("\tR11   = " << HEX(8, reg[R11])   << endl);
    DBG("\tR12   = " << HEX(8, reg[R12])   << endl);
    DBG("\tFLAGS = " << HEX(8, reg[FLAGS]) << endl);
    DBG("\tSP    = " << HEX(8, reg[SP])    << endl);
    DBG("\tPC    = " << HEX(8, reg[PC])    << endl);
}
