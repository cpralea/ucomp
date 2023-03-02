$sys_enter:
    jmp $sys_enter
    load r1, [r2]
    store [r2], r1
