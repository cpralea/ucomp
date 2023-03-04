#pragma once


#include <cstddef>


typedef enum {
    INTERPRETER = 1
} exec_type_t;


extern "C" void vm_run(const void* prog, size_t prog_size, size_t ram_size_mb, exec_type_t exec_type);
