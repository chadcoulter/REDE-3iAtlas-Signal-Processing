.section .text
.globl _start
_start:
    call tanakh_transform
    movq $1, %rax
    movq $1, %rdi
    leaq state(%rip), %rsi
    movq $64, %rdx
    syscall
    movq $60, %rax
    xorq %rdi, %rdi
    syscall
.section .note.GNU-stack,"",@progbits
