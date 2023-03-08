;
; Compute 16th Fibonacci number using
;
;     fibonacci(n) {
;         if (n <= 1)
;             return n;
;         return fibonacci(n-2) + fibonacci(n-1);
;     }
;

main:
    mov r0, 16
    push r0
    call fibonacci

    mov r0, 1
    push r0
    call $sys_enter

    add sp, 8

    mov r0, 0
    push r0
    call $sys_enter

fibonacci:
    load r12, [sp]

    mov r0, sp
    add r0, 4
    load r0, [r0]

    cmp r0, 1
    jmple .return

    push r12

    mov r1, r0
    sub r1, 1
    push r1
    mov r2, r0
    sub r2, 2
    push r2

    call fibonacci
    pop r2
    pop r1
    push r2
    push r1
    call fibonacci
    pop r1
    pop r2
    
    mov r0, 0
    add r0, r1
    add r0, r2

    pop r12

.return:
    add sp, 8
    push r0
    push r12
    ret
