; bitwise_shift.asm

; --- Initialisierung ---
MOV R0, #3          ; R0 = 3 (00000011 in binär)

; --- Shift Left ---
SHL R1, R0, #2      ; R1 = R0 << 2 = 12 (00001100)
OUT #0, R1          ; Ausgabe von R1 (12)

; --- Shift Right ---
SHR R2, R0, #1      ; R2 = R0 >> 1 = 1 (00000001)
OUT #0, R2          ; Ausgabe von R2 (1)

; --- Programm beenden ---
HALT
