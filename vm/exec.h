#pragma once


#include <cstddef>
#include <cstdint>


class ExecutionEngine {
protected:
    const void* prog;
    size_t prog_size;
    size_t ram_size;

public:
    ExecutionEngine(const void* prog, size_t prog_size, size_t ram_size_mb)
        : prog(prog), prog_size(prog_size), ram_size(ram_size_mb << 20) {}
    virtual ~ExecutionEngine() {}

    virtual void execute() = 0;
};


class Interpreter : public ExecutionEngine {
    uint8_t* ram;

public:
    Interpreter(const void* prog, size_t prog_size, size_t ram_size_mb)
        : ExecutionEngine(prog, prog_size, ram_size_mb), ram(nullptr) {}
    ~Interpreter();

    void execute();
};
