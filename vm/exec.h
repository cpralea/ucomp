#pragma once


#include <cstddef>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <memory>


using std::cout, std:: endl;


#define DEBUG(DATA) { if (debug) cout << "[DEBUG] " << DATA; }
#define HEX(WIDTH) std::setw(WIDTH) << std::setfill('0') << std::right << std::hex << std::noshowbase


class ExecutionEngine {
protected:
    const void* prog;
    size_t prog_size;
    size_t ram_size;
    bool debug;

    struct {
        int64_t R0;
        int64_t R1;
        int64_t R2;
        int64_t R3;
        int64_t R4;
        int64_t R5;
        int64_t R6;
        int64_t R7;
        int64_t R8;
        int64_t R9;
        int64_t R10;
        int64_t R11;
        int64_t R12;
        uint64_t FLAGS;
        uint64_t SP;
        uint64_t PC;
    } register_file;

public:
    ExecutionEngine(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
        : prog(prog), prog_size(prog_size), ram_size(ram_size_mb << 20), debug(debug) {
            DEBUG("Initializing VM with:" << endl);
            DEBUG("\tprogram at 0x" << HEX(16) << prog << ", size " << prog_size << endl);
            DEBUG("\tmemory " << ram_size_mb << " MiB" << endl);
        }
    virtual ~ExecutionEngine() {}

    virtual void init() = 0;
    virtual void load() = 0;
    virtual void run() = 0;
    virtual void fini() = 0;

    virtual void execute() final {
        init();
        load();
        run();
        fini();
    }

protected:
    void dump_registers() const {
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
};


class Interpreter : public ExecutionEngine {
    std::unique_ptr<uint8_t[]> ram;

public:
    Interpreter(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug);

    void init();
    void load();
    void run();
    void fini();
};
