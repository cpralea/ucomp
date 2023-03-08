;
; Compute 12! using
;
;     factorial(n) {
;         if (n <= 1)
;             return 1;
;         return n * factorial(n-1);
;     }
;

main:
    mov r0, 12
    push r0
    call factorial

    mov r0, 1
    push r0
    call $sys_enter

    add sp, 8

    mov r0, 0
    push r0
    call $sys_enter

factorial:
    load r12, [sp]

    mov r0, sp
    add r0, 4
    load r1, [r0]

    mov r0, r1
    cmp r0, 1
    jmpeq .return

    push r12

    push r0
    sub r0, 1
    push r0
    call factorial
    call multiply
    pop r0

    pop r12

.return:
    add sp, 8
    push r0
    push r12
    ret

multiply:
    load r12, [sp]

    mov r0, sp;
    add r0, 8
    load r1, [r0];
    sub r0, 4
    load r2, [r0]

    cmp r2, r1
    jmple .do_multiply
    mov r3, r1
    mov r1, r2
    mov r2, r3

.do_multiply:
    mov r0, 0
.loop:
    cmp r2, 0
    jmpz .return
    add r0, r1
    sub r2, 1
    jmp .loop

.return:
    add sp, 12
    push r0
    push r12
    ret
