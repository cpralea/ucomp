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
    ExecutionEngine(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug);
    virtual ~ExecutionEngine();

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
    void dump_registers() const;
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
