; test_basic.asm

; --- Initialisierung ---
MOV R0, #10        ; R0 = 10
MOV R1, #20        ; R1 = 20

; --- Arithmetische Operationen ---
ADD R2, R0, R1     ; R2 = R0 + R1 (30)
SUB R3, R1, R0     ; R3 = R1 - R0 (10)

; --- Logische Operationen ---
AND R4, R0, R1     ; R4 = R0 AND R1 (0)
OR R5, R0, R1      ; R5 = R0 OR R1 (30)
XOR R6, R0, R1     ; R6 = R0 XOR R1 (30)
NOT R7, R6         ; R7 = NOT R6 (-31)

; --- Vergleich und Sprünge ---
CMP R0, R1         ; Vergleiche R0 mit R1
JE EQUAL_LABEL     ; Springe zu EQUAL_LABEL, wenn R0 == R1
JNE NOT_EQUAL_LABEL ; Springe zu NOT_EQUAL_LABEL, wenn R0 != R1

EQUAL_LABEL:
MOV R0, #1         ; R0 = 1
JMP END_LABEL

NOT_EQUAL_LABEL:
MOV R0, #0         ; R0 = 0

END_LABEL:
; --- Stapeloperationen ---
PUSH R0            ; Schiebe R0 auf den Stack
POP R1             ; Hole Wert vom Stack nach R1

; --- Eingabe/Ausgabe ---
IN R2, #0          ; Lese Eingabe vom Benutzer in R2
OUT #0, R2         ; Ausgabe von R2 an Port 0

; --- Textausgabe ---
; Länge der Zeichenkette festlegen
MOV R3, #15        ; R3 = 15 (Länge der Zeichenkette)

; Adresse der Zeichenkette in R4 laden
MOV R4, DATA_START ; R4 = Adresse von DATA_START

; Text ausgeben
PRINT R4, R3       ; Gib die Zeichenkette aus

; --- Programm beenden ---
HALT                 ; Programm beenden

; --- Datenbereich ---
DATA_START:
DB 'Basic ASM Test!', 0  ; Zeichenkette mit Nullterminierung
