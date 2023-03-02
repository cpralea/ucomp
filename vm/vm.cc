#include <cstddef>
#include <iostream>
#include <iomanip>

#include "vm.h"

using std::cout, std::endl;


extern "C" void vm_run(const void* prog, size_t prog_size, size_t ram_size_mb)
{
    cout << "ram size: " << ram_size_mb << " MiB" << endl;
    
    for (size_t i = 0; i < prog_size; i++)
        cout
            << std::setw(2) << std::setfill('0') << std::right << std::hex
            << (int) *(((char*) prog) + i)
            << ' ';
    cout << endl;
}
