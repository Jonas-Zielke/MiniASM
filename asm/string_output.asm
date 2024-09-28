; string_output.asm

; --- Initialisierung ---
MOV R0, DATA_STRING ; R0 = Adresse des Strings
MOV R1, #14         ; R1 = Länge des Strings

; --- String ausgeben ---
PRINT R0, R1         ; Ausgabe des Strings

; --- Programm beenden ---
HALT

; --- Datenbereich ---
DATA_STRING:
    DB 'Hello, MiniASM!', 0  ; Nullterminierter String
