; conditional_jump.asm

; --- Initialisierung ---
MOV R0, #10        ; R0 = 10
MOV R1, #10        ; R1 = 10

; --- Vergleich ---
CMP R0, R1         ; Vergleiche R0 mit R1

; --- Bedingte Sprünge ---
JE EQUAL_LABEL     ; Springe zu EQUAL_LABEL, wenn R0 == R1
JNE NOT_EQUAL_LABEL ; Springe zu NOT_EQUAL_LABEL, wenn R0 != R1

; --- Label: EQUAL_LABEL ---
EQUAL_LABEL:
    MOV R2, #1     ; R2 = 1 (Egalheit bestätigt)
    OUT #0, R2     ; Ausgabe von R2 (1)
    JMP END_LABEL

; --- Label: NOT_EQUAL_LABEL ---
NOT_EQUAL_LABEL:
    MOV R2, #0     ; R2 = 0 (Keine Egalheit)
    OUT #0, R2     ; Ausgabe von R2 (0)

; --- Label: END_LABEL ---
END_LABEL:
    HALT
