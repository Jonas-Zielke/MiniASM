; fibonacci.asm

; --- Initialisierung ---
MOV R0, #0         ; R0 = F(n-2) = 0
MOV R1, #1         ; R1 = F(n-1) = 1
MOV R2, #10        ; R2 = Anzahl der Fibonacci-Zahlen (10)

; --- Fibonacci Loop ---
FIB_LOOP:
    CMP R2, #0
    JE FIB_END          ; Wenn R2 == 0, beende die Schleife
    OUT #0, R0          ; Ausgabe von R0 (F(n-2))
    ADD R3, R0, R1      ; R3 = F(n) = F(n-2) + F(n-1)
    MOV R0, R1          ; R0 = F(n-1)
    MOV R1, R3          ; R1 = F(n)
    SUB R2, R2, #1      ; R2 = R2 - 1
    JMP FIB_LOOP        ; Springe zurück zu FIB_LOOP

; --- Fibonacci End ---
FIB_END:
    HALT
