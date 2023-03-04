#pragma once


#include <cstddef>
#include <cstdint>
#include <iostream>
#include <memory>


using std::cout, std:: endl;


#define DEBUG(DATA) { if (debug) cout << "[DEBUG] " << DATA; }


class ExecutionEngine {
protected:
    const void* prog;
    size_t prog_size;
    size_t ram_size;
    bool debug;

public:
    ExecutionEngine(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug)
        : prog(prog), prog_size(prog_size), ram_size(ram_size_mb << 20), debug(debug) {
            DEBUG("Initializing VM with:" << endl);
            DEBUG("\tprogram at " << std::hex << std::showbase << prog << ", size " << prog_size << endl);
            DEBUG("\tmemory " << ram_size_mb << " MiB" << endl);
        }
    virtual ~ExecutionEngine() {}

    virtual void execute() = 0;
};


class Interpreter : public ExecutionEngine {
    std::unique_ptr<uint8_t[]> ram;

public:
    Interpreter(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug);

    void execute();
};
