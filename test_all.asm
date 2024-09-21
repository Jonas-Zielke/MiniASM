; test_all.asm

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
JMP CONTINUE_LABEL ; Ansonsten weiter zu CONTINUE_LABEL

EQUAL_LABEL:
MOV R0, #1         ; R0 = 1 (wird hier nicht ausgeführt)

CONTINUE_LABEL:
; --- Stapeloperationen ---
PUSH R0            ; Schiebe R0 auf den Stack
POP R1             ; Hole Wert vom Stack nach R1

; --- Eingabe/Ausgabe ---
IN R3, #0          ; Lese Eingabe vom Benutzer in R3
OUT #0, R3         ; Ausgabe von R3 an Port 0

; --- Textausgabe ---
; Länge der Zeichenkette festlegen
MOV R5, #15        ; R5 = 15

; Adresse der Zeichenkette in R4 laden
MOV R4, DATA_START ; R4 = Adresse von DATA_START

; Text ausgeben
PRINT R4, R5       ; Gib die Zeichenkette aus

; --- Dateioperationen ---
; Öffne eine Datei zum Schreiben
MOV R0, FILENAME   ; R0 = Adresse des Dateinamens
MOV R1, #1         ; R1 = Modus 1 (Schreiben)
MOV R2, #0         ; R2 = Dateideskriptor (wird in OPEN gesetzt)
OPEN R0, R1, R2    ; Öffne die Datei zum Schreiben

; Schreibe eine Nachricht in die Datei
MOV R3, MESSAGE    ; R3 = Adresse der Nachricht
MOV R4, #27        ; R4 = Länge der Nachricht
WRITE R2, R3, R4   ; Schreibe die Nachricht in die Datei

; Schließe die Datei
CLOSE R2           ; Schließe die Datei

; --- Benchmark ---
; Führe eine große Anzahl von Operationen durch, um die Leistung zu messen.

MOV R6, #0         ; Zähler initialisieren (R6 = 0)
MOV R7, #50000     ; Anzahl der Iterationen (R7 = 50.000)

BENCHMARK_LOOP:
ADD R6, R6, #1     ; R6 = R6 + 1
MUL R5, R6, R6     ; R5 = R6 * R6
DIV R5, R5, R6     ; R5 = R5 / R6 (ergibt wieder R6)
CMP R6, R7         ; Vergleiche R6 mit R7
JL BENCHMARK_LOOP  ; Springe zu BENCHMARK_LOOP, wenn R6 < R7

; --- Programm beenden ---
HALT               ; Programm beenden

; --- Datenbereich ---
DATA_START:
DB 'Hallo, MINI ASM!'  ; Zeichenkette mit Nullterminierung

FILENAME:
DB 'output.txt', 0     ; Dateiname mit Nullterminierung

MESSAGE:
DB 'Dies ist eine Testnachricht.', 0 ; Nachricht mit Nullterminierung
