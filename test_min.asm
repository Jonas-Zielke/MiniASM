; test_min.asm

; --- Programmcode ---

; Länge der Zeichenkette festlegen
MOV R5, 15         ; R5 = 15 (Länge der Zeichenkette)

; Adresse der Zeichenkette in R4 laden
MOV R4, DATA_START ; R4 = Adresse von DATA_START

; Text ausgeben
PRINT R4, R5       ; Gib die Zeichenkette aus

; Programm beenden
HALT               ; Beendet das Programm

; --- Datenbereich ---
DATA_START:
DB 'Hallo, MINI ASM!'  ; Zeichenkette mit Nullterminierung
