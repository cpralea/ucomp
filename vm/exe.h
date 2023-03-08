#pragma once


#include <cstddef>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <memory>


using std::cout, std:: endl;


#define DBG_(DATA) { if (debug) { cout << DATA; } }
#define DBG(DATA) DBG_("[DEBUG] " << DATA)
#define HEX_(WIDTH, DATA) \
    std::setw(WIDTH) << \
    std::setfill('0') << std::right << std::hex << std::noshowbase << DATA << \
    std::dec
#define HEX(WIDTH, DATA) "0x" << HEX_(WIDTH, DATA)

class ExecutionEngine {
protected:
    const void* prog;
    size_t prog_size;
    size_t ram_size;
    bool debug;

    std::unique_ptr<uint8_t[]> mem;
    uint32_t reg[16];

    virtual void init_execution() = 0;
    virtual void load_program() = 0;
    virtual void exec_program() = 0;
    virtual void fini_execution() = 0;

public:
    ExecutionEngine(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug);
    virtual ~ExecutionEngine();

    virtual void execute() final {
        init_execution();
        load_program();
        exec_program();
        fini_execution();
    }

protected:
    typedef enum : uint8_t {
        LOAD    =  1,
        STORE   =  2,
        MOV     =  3,
        ADD     =  4,
        SUB     =  5,
        AND     =  6,
        OR      =  7,
        XOR     =  8,
        NOT     =  9,
        CMP     = 10,
        PUSH    = 11,
        POP     = 12,
        CALL    = 13,
        RET     = 14,
        JMP     = 15,
        JMPZ    = 16,
        JMPNZ   = 17,
        JMPEQ   = 18,
        JMPNE   = 19,
        JMPGT   = 20,
        JMPLT   = 21,
        JMPGE   = 22,
        JMPLE   = 23
    } instruction_t;
    
    typedef enum : uint8_t {
        R0      =  0,
        R1      =  1,
        R2      =  2,
        R3      =  3,
        R4      =  4,
        R5      =  5,
        R6      =  6,
        R7      =  7,
        R8      =  8,
        R9      =  9,
        R10     = 10,
        R11     = 11,
        R12     = 12,
        FLAGS   = 13,
        SP      = 14,
        PC      = 15
    } register_t;

    typedef enum : uint8_t {
        REG     =  0,
        IMM     =  1
    } reg_imm_t;

    static const uint32_t SYS_ENTER_ADDR    = 0x0;
    static const uint32_t SYSCALL_VM_EXIT   = 0;

    static const uint32_t FLAG_Z            = 0b00000001;
    static const uint32_t FLAG_EQ           = 0b00000010;
    static const uint32_t FLAG_LT           = 0b00000100;
    static const uint32_t FLAG_GT           = 0x00001000;

    static const uint8_t OPCODE_MASK        = 0xfe;
    static const uint8_t REG_IMM_MASK       = 0x01;
    static const uint8_t REG_DST_MASK       = 0xf0;
    static const uint8_t REG_SRC_MASK       = 0x0f;

    static uint8_t instr(uint8_t byte) { return (byte & OPCODE_MASK) >> 1; }
    static uint8_t reg_imm(uint8_t byte) { return byte & REG_IMM_MASK; }
    static uint8_t reg_dst(uint8_t byte) { return (byte & REG_DST_MASK) >> 4; }
    static uint8_t reg_src(uint8_t byte) { return byte & REG_SRC_MASK; }
    static uint32_t imm_val(const uint8_t& data) { return uint8_to_uint32(const_cast<uint8_t&>(data)); }

    static int32_t& uint32_to_int32(uint32_t& val) { return reinterpret_cast<int32_t&>(val); }
    static uint32_t& uint8_to_uint32(uint8_t& val) { return reinterpret_cast<uint32_t&>(val); }

    void dump_registers() const;
};


class Interpreter final : public ExecutionEngine {
public:
    Interpreter(const void* prog, size_t prog_size, size_t ram_size_mb, bool debug);

private:
    void init_execution();
    void load_program();
    void exec_program();
    void fini_execution();

    void sys_enter();

    void trace(uint8_t ri, uint8_t dst, uint8_t src, uint32_t iv) const;
};
