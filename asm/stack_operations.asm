; stack_operations.asm

; --- Initialisierung ---
MOV R0, #100       ; R0 = 100
MOV R1, #200       ; R1 = 200

; --- Stack Operationen ---
PUSH R0            ; Schiebe R0 (100) auf den Stack
PUSH R1            ; Schiebe R1 (200) auf den Stack

; --- Pop Operationen ---
POP R2             ; Hole 200 vom Stack nach R2
OUT #0, R2         ; Ausgabe von R2 (200)

POP R3             ; Hole 100 vom Stack nach R3
OUT #0, R3         ; Ausgabe von R3 (100)

; --- Programm beenden ---
HALT
