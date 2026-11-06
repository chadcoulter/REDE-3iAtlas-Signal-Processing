# Generated using Hebrew gematria -> Atlas Greek numerals -> archived operators.
# Every source letter is dispatched. Five-letter 2+3 roles remain an unexecuted hypothesis.
.section .data
.balign 8
state:
    .quad 1
relations:
    .quad 1
constraints:
    .quad 1
observations:
    .quad 1
unresolved:
    .quad 1
context:
    .quad 1
target:
    .quad 1
events:
    .quad 1
.section .text
.globl tanakh_transform
tanakh_transform:
    # index=0 Hebrew=ד value=4 Greek=Δ
    incq state(%rip)
    # index=1 Hebrew=ב value=2 Greek=Β
    incq context(%rip)
    # index=2 Hebrew=ר value=200 Greek=Σ
    movq relations(%rip), %rax
    addq %rax, state(%rip)
    incq state(%rip)
    # index=3 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=4 Hebrew=ע value=70 Greek=Ο
    movq state(%rip), %rax
    xorq relations(%rip), %rax
    addq %rax, observations(%rip)
    # index=5 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=6 Hebrew=ו value=6 Greek=Ϛ
    incq unresolved(%rip)
    # index=7 Hebrew=ס value=60 Greek=Ξ
    movq state(%rip), %rax
    xorq target(%rip), %rax
    addq %rax, unresolved(%rip)
    # index=8 Hebrew=א value=1 Greek=Α
    movq $1, state(%rip)
    # index=9 Hebrew=ש value=300 Greek=Τ
    movq state(%rip), %rax
    addq relations(%rip), %rax
    addq constraints(%rip), %rax
    movq %rax, target(%rip)
    # index=10 Hebrew=ר value=200 Greek=Σ
    movq relations(%rip), %rax
    addq %rax, state(%rip)
    incq state(%rip)
    # index=11 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    # index=12 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=13 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    # index=14 Hebrew=ב value=2 Greek=Β
    incq context(%rip)
    # index=15 Hebrew=ן value=50 Greek=Ν
    movq state(%rip), %rax
    incq %rax
    movq %rax, target(%rip)
    # index=16 Hebrew=ק value=100 Greek=Ρ
    movq target(%rip), %rax
    xorq %rax, relations(%rip)
    # index=17 Hebrew=ד value=4 Greek=Δ
    incq state(%rip)
    # index=18 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=19 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=20 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=21 Hebrew=ת value=400 Greek=Υ
    movq constraints(%rip), %rax
    testq $1, %rax
    jz 1f
    incq context(%rip)
    jmp 2f
    1:
    incq relations(%rip)
    2:
    # index=22 Hebrew=ק value=100 Greek=Ρ
    movq target(%rip), %rax
    xorq %rax, relations(%rip)
    # index=23 Hebrew=ו value=6 Greek=Ϛ
    incq unresolved(%rip)
    # index=24 Hebrew=ע value=70 Greek=Ο
    movq state(%rip), %rax
    xorq relations(%rip), %rax
    addq %rax, observations(%rip)
    # index=25 Hebrew=א value=1 Greek=Α
    movq $1, state(%rip)
    # index=26 Hebrew=ש value=300 Greek=Τ
    movq state(%rip), %rax
    addq relations(%rip), %rax
    addq constraints(%rip), %rax
    movq %rax, target(%rip)
    # index=27 Hebrew=ר value=200 Greek=Σ
    movq relations(%rip), %rax
    addq %rax, state(%rip)
    incq state(%rip)
    # index=28 Hebrew=ח value=8 Greek=Η
    movq state(%rip), %rax
    movq %rax, target(%rip)
    # index=29 Hebrew=ז value=7 Greek=Ζ
    movq state(%rip), %rax
    xorq %rax, relations(%rip)
    # index=30 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    # index=31 Hebrew=ע value=70 Greek=Ο
    movq state(%rip), %rax
    xorq relations(%rip), %rax
    addq %rax, observations(%rip)
    # index=32 Hebrew=ל value=30 Greek=Λ
    movq relations(%rip), %rax
    xorq %rax, state(%rip)
    # index=33 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=34 Hebrew=ש value=300 Greek=Τ
    movq state(%rip), %rax
    addq relations(%rip), %rax
    addq constraints(%rip), %rax
    movq %rax, target(%rip)
    # index=35 Hebrew=ר value=200 Greek=Σ
    movq relations(%rip), %rax
    addq %rax, state(%rip)
    incq state(%rip)
    # index=36 Hebrew=א value=1 Greek=Α
    movq $1, state(%rip)
    # index=37 Hebrew=ל value=30 Greek=Λ
    movq relations(%rip), %rax
    xorq %rax, state(%rip)
    # index=38 Hebrew=ב value=2 Greek=Β
    incq context(%rip)
    # index=39 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=40 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=41 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=42 Hebrew=ע value=70 Greek=Ο
    movq state(%rip), %rax
    xorq relations(%rip), %rax
    addq %rax, observations(%rip)
    # index=43 Hebrew=ז value=7 Greek=Ζ
    movq state(%rip), %rax
    xorq %rax, relations(%rip)
    # index=44 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=45 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    # index=46 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=47 Hebrew=ל value=30 Greek=Λ
    movq relations(%rip), %rax
    xorq %rax, state(%rip)
    # index=48 Hebrew=ך value=20 Greek=Κ
    incq context(%rip)
    # index=49 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=50 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    # index=51 Hebrew=ו value=6 Greek=Ϛ
    incq unresolved(%rip)
    # index=52 Hebrew=ד value=4 Greek=Δ
    incq state(%rip)
    # index=53 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    # index=54 Hebrew=ו value=6 Greek=Ϛ
    incq unresolved(%rip)
    # index=55 Hebrew=ב value=2 Greek=Β
    incq context(%rip)
    # index=56 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=57 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=58 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=59 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=60 Hebrew=ר value=200 Greek=Σ
    movq relations(%rip), %rax
    addq %rax, state(%rip)
    incq state(%rip)
    # index=61 Hebrew=ב value=2 Greek=Β
    incq context(%rip)
    # index=62 Hebrew=ע value=70 Greek=Ο
    movq state(%rip), %rax
    xorq relations(%rip), %rax
    addq %rax, observations(%rip)
    # index=63 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=64 Hebrew=ב value=2 Greek=Β
    incq context(%rip)
    # index=65 Hebrew=ן value=50 Greek=Ν
    movq state(%rip), %rax
    incq %rax
    movq %rax, target(%rip)
    # index=66 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=67 Hebrew=ו value=6 Greek=Ϛ
    incq unresolved(%rip)
    # index=68 Hebrew=א value=1 Greek=Α
    movq $1, state(%rip)
    # index=69 Hebrew=ש value=300 Greek=Τ
    movq state(%rip), %rax
    addq relations(%rip), %rax
    addq constraints(%rip), %rax
    movq %rax, target(%rip)
    # index=70 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=71 Hebrew=ל value=30 Greek=Λ
    movq relations(%rip), %rax
    xorq %rax, state(%rip)
    # index=72 Hebrew=ך value=20 Greek=Κ
    incq context(%rip)
    # index=73 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=74 Hebrew=ש value=300 Greek=Τ
    movq state(%rip), %rax
    addq relations(%rip), %rax
    addq constraints(%rip), %rax
    movq %rax, target(%rip)
    # index=75 Hebrew=ר value=200 Greek=Σ
    movq relations(%rip), %rax
    addq %rax, state(%rip)
    incq state(%rip)
    # index=76 Hebrew=א value=1 Greek=Α
    movq $1, state(%rip)
    # index=77 Hebrew=ל value=30 Greek=Λ
    movq relations(%rip), %rax
    xorq %rax, state(%rip)
    # index=78 Hebrew=ש value=300 Greek=Τ
    movq state(%rip), %rax
    addq relations(%rip), %rax
    addq constraints(%rip), %rax
    movq %rax, target(%rip)
    # index=79 Hebrew=ן value=50 Greek=Ν
    movq state(%rip), %rax
    incq %rax
    movq %rax, target(%rip)
    # index=80 Hebrew=ת value=400 Greek=Υ
    movq constraints(%rip), %rax
    testq $1, %rax
    jz 1f
    incq context(%rip)
    jmp 2f
    1:
    incq relations(%rip)
    2:
    # index=81 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=82 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=83 Hebrew=ל value=30 Greek=Λ
    movq relations(%rip), %rax
    xorq %rax, state(%rip)
    # index=84 Hebrew=ף value=80 Greek=Π
    movq state(%rip), %rax
    addq context(%rip), %rax
    movq %rax, target(%rip)
    # index=85 Hebrew=ן value=50 Greek=Ν
    movq state(%rip), %rax
    incq %rax
    movq %rax, target(%rip)
    # index=86 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=87 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    # index=88 Hebrew=ר value=200 Greek=Σ
    movq relations(%rip), %rax
    addq %rax, state(%rip)
    incq state(%rip)
    # index=89 Hebrew=ע value=70 Greek=Ο
    movq state(%rip), %rax
    xorq relations(%rip), %rax
    addq %rax, observations(%rip)
    # index=90 Hebrew=ש value=300 Greek=Τ
    movq state(%rip), %rax
    addq relations(%rip), %rax
    addq constraints(%rip), %rax
    movq %rax, target(%rip)
    # index=91 Hebrew=ו value=6 Greek=Ϛ
    incq unresolved(%rip)
    # index=92 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=93 Hebrew=א value=1 Greek=Α
    movq $1, state(%rip)
    # index=94 Hebrew=ם value=40 Greek=Μ
    movq state(%rip), %rax
    addq %rax, observations(%rip)
    # index=95 Hebrew=ר value=200 Greek=Σ
    movq relations(%rip), %rax
    addq %rax, state(%rip)
    incq state(%rip)
    # index=96 Hebrew=י value=10 Greek=Ι
    incq events(%rip)
    # index=97 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    # index=98 Hebrew=ו value=6 Greek=Ϛ
    incq unresolved(%rip)
    # index=99 Hebrew=ה value=5 Greek=Ε
    cmpq $0, constraints(%rip)
    sete %al
    movzbq %al, %rax
    addq %rax, observations(%rip)
    ret
.section .note.GNU-stack,"",@progbits
