; logical.asm

; --- Initialisierung ---
MOV R0, #12        ; R0 = 12 (1100 in binär)
MOV R1, #10        ; R1 = 10 (1010 in binär)

; --- AND Operation ---
AND R2, R0, R1     ; R2 = R0 AND R1 (8)
OUT #0, R2         ; Ausgabe von R2 (8)

; --- OR Operation ---
OR R3, R0, R1      ; R3 = R0 OR R1 (14)
OUT #0, R3         ; Ausgabe von R3 (14)

; --- XOR Operation ---
XOR R4, R0, R1     ; R4 = R0 XOR R1 (6)
OUT #0, R4         ; Ausgabe von R4 (6)

; --- NOT Operation ---
NOT R5, R0         ; R5 = NOT R0 (-13)
OUT #0, R5         ; Ausgabe von R5 (-13)

; --- Programm beenden ---
HALT
