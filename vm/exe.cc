#include "exe.h"


ExecutionEngine::ExecutionEngine(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
: prog(prog), prog_size(prog_size), ram_size(ram_size_mb << 20), debug(debug)
{
    DEBUG("Initializing VM with:" << endl);
    DEBUG("\tprogram at 0x" << HEX(16) << prog << ", size " << prog_size << endl);
    DEBUG("\tmemory " << ram_size_mb << " MiB" << endl);
}


ExecutionEngine::~ExecutionEngine()
{
}


void ExecutionEngine::dump_registers() const
{
    DEBUG("Registers:" << endl);
    DEBUG("\tR0    = 0x" << HEX(16) << register_file.R0    << endl);
    DEBUG("\tR1    = 0x" << HEX(16) << register_file.R1    << endl);
    DEBUG("\tR2    = 0x" << HEX(16) << register_file.R2    << endl);
    DEBUG("\tR3    = 0x" << HEX(16) << register_file.R3    << endl);
    DEBUG("\tR4    = 0x" << HEX(16) << register_file.R4    << endl);
    DEBUG("\tR5    = 0x" << HEX(16) << register_file.R5    << endl);
    DEBUG("\tR6    = 0x" << HEX(16) << register_file.R6    << endl);
    DEBUG("\tR7    = 0x" << HEX(16) << register_file.R7    << endl);
    DEBUG("\tR8    = 0x" << HEX(16) << register_file.R8    << endl);
    DEBUG("\tR9    = 0x" << HEX(16) << register_file.R9    << endl);
    DEBUG("\tR10   = 0x" << HEX(16) << register_file.R10   << endl);
    DEBUG("\tR11   = 0x" << HEX(16) << register_file.R11   << endl);
    DEBUG("\tR12   = 0x" << HEX(16) << register_file.R12   << endl);
    DEBUG("\tFLAGS = 0x" << HEX(16) << register_file.FLAGS << endl);
    DEBUG("\tSP    = 0x" << HEX(16) << register_file.SP    << endl);
    DEBUG("\tPC    = 0x" << HEX(16) << register_file.PC    << endl);
}
