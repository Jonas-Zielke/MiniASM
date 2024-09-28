; test_full.asm

; --- Initialisierung ---
MOV R0, #10        ; R0 = 10
MOV R1, #20        ; R1 = 20

; --- Arithmetische Operationen ---
ADD R2, R0, R1     ; R2 = R0 + R1 (30)
SUB R3, R1, R0     ; R3 = R1 - R0 (10)
MUL R4, R0, R1     ; R4 = R0 * R1 (200)
DIV R5, R1, R0     ; R5 = R1 / R0 (2)

; --- Logische Operationen ---
AND R6, R0, R1     ; R6 = R0 AND R1 (0)
OR R7, R0, R1      ; R7 = R0 OR R1 (30)
XOR R0, R0, R1     ; R0 = R0 XOR R1 (30)
NOT R1, R0         ; R1 = NOT R0 (-31)
SHL R2, R2, #2     ; R2 = R2 << 2 (120)
SHR R3, R3, #1     ; R3 = R3 >> 1 (5)

; --- Vergleich und Sprünge ---
CMP R0, R1         ; Vergleich von R0 und R1
JE EQUAL_LABEL     ; Springe zu EQUAL_LABEL, wenn R0 == R1
JNE NOT_EQUAL_LABEL ; Springe zu NOT_EQUAL_LABEL, wenn R0 != R1

EQUAL_LABEL:
MOV R0, #1         ; R0 = 1
JMP CONTINUE_LABEL

NOT_EQUAL_LABEL:
MOV R0, #0         ; R0 = 0

CONTINUE_LABEL:
; --- Stapeloperationen ---
PUSH R0            ; Schiebe R0 auf den Stack
POP R1             ; Hole Wert vom Stack nach R1

; --- Eingabe/Ausgabe ---
IN R3, #0          ; Lese Eingabe vom Benutzer in R3
OUT #0, R3         ; Ausgabe von R3 an Port 0

; --- Textausgabe ---
; Länge der Zeichenkette festlegen
MOV R5, #17        ; R5 = 17 (Länge der Zeichenkette)

; Adresse der Zeichenkette in R4 laden
MOV R4, DATA_START ; R4 = Adresse von DATA_START

; Text ausgeben
PRINT R4, R5       ; Gib die Zeichenkette aus

; --- Programm beenden ---
HALT                 ; Programm beenden

; --- Datenbereich ---
DATA_START:
DB 'Hallo, MINI ASM!', 0  ; Zeichenkette mit Nullterminierung
