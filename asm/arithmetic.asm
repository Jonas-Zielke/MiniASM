; arithmetic.asm

; --- Initialisierung ---
MOV R0, #15        ; R0 = 15
MOV R1, #5         ; R1 = 5

; --- Addition ---
ADD R2, R0, R1     ; R2 = R0 + R1 (20)
OUT #0, R2         ; Ausgabe von R2 (20)

; --- Subtraktion ---
SUB R3, R0, R1     ; R3 = R0 - R1 (10)
OUT #0, R3         ; Ausgabe von R3 (10)

; --- Multiplikation ---
MUL R4, R0, R1     ; R4 = R0 * R1 (75)
OUT #0, R4         ; Ausgabe von R4 (75)

; --- Division ---
DIV R5, R0, R1     ; R5 = R0 / R1 (3)
OUT #0, R5         ; Ausgabe von R5 (3)

; --- Programm beenden ---
HALT
