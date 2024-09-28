; factorial.asm

; --- Initialisierung ---
MOV R0, #5         ; R0 = Zahl für Fakultät (5)
MOV R1, #1         ; R1 = Ergebnis starten bei 1

; --- Factorial Loop ---
FACTORIAL_LOOP:
    CMP R0, #1         ; Vergleiche R0 mit 1
    JL FACTORIAL_END   ; Wenn R0 < 1, springe zu FACTORIAL_END
    MUL R1, R1, R0     ; R1 = R1 * R0
    SUB R0, R0, #1     ; R0 = R0 - 1
    JMP FACTORIAL_LOOP ; Springe zurück zu FACTORIAL_LOOP

; --- Factorial End ---
FACTORIAL_END:
    OUT #0, R1         ; Ausgabe des Ergebnisses
    HALT
