; loop.asm

; --- Initialisierung ---
MOV R0, #1         ; R0 = Zähler starten bei 1
MOV R1, #5         ; R1 = Endwert 5

; --- Loop Start ---
LOOP_START:
    CMP R0, R1         ; Vergleiche R0 mit R1
    JG LOOP_END        ; Wenn R0 > R1, springe zu LOOP_END
    OUT #0, R0         ; Ausgabe von R0
    ADD R0, R0, #1     ; Erhöhe R0 um 1
    JMP LOOP_START     ; Springe zurück zu LOOP_START

; --- Loop End ---
LOOP_END:
    HALT
