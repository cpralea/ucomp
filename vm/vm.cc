#include <cstddef>
#include <cstdlib>
#include <memory>

#include "vm.h"
#include "exec.h"


static size_t adjust_ram_size_mb(size_t ram_size_mb);
static ExecutionEngine* create_execution_engine(
    const void* prog, size_t prog_size, size_t ram_size_mb, exec_type_t exec_type);


extern "C" void vm_run(const void* prog, size_t prog_size, size_t ram_size_mb, exec_type_t exec_type)
{
    std::unique_ptr<ExecutionEngine>(
        create_execution_engine(
            prog,
            prog_size,
            adjust_ram_size_mb(ram_size_mb),
            exec_type
    ))->execute();
}


static size_t adjust_ram_size_mb(size_t ram_size_mb)
{
    size_t size = 0x4;
    while (ram_size_mb > size)
        size <<= 1;
    return size;
}


static ExecutionEngine* create_execution_engine(
    const void* prog, size_t prog_size, size_t ram_size_mb, exec_type_t exec_type)
{
    switch (exec_type) {
    case INTERPRETER:
        return new Interpreter(prog, prog_size, ram_size_mb);
    default:
        std::abort();
    }
}
