import os
import time
import json
import numpy as np
import matplotlib.pyplot as plt

# Display-Spezifikationen
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 128

# Speicher und Register
RAM = np.zeros(100 * 1024 * 1024, dtype=np.uint8)  # 100 MB RAM
DISK = np.zeros(10 * 1024 * 1024 * 1024, dtype=np.uint8)  # 10 GB Disk
registers = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'ACC': 0, 'PC': 0, 'SP': 0}
flags = {'ZF': 0}
stack = []
loop_start = None
loop_condition = True

# Display
display = np.zeros((DISPLAY_WIDTH, DISPLAY_HEIGHT), dtype=np.uint8)

# Befehle aus der JSON-Konfigurationsdatei laden
with open('commands.json', 'r') as f:
    commands = json.load(f)


# Funktion zum Abrufen eines Wertes (Register oder direkte Zahl)
def get_value(operand):
    if operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
        return int(operand)
    elif operand in registers:
        return registers[operand]
    else:
        raise ValueError(f"Ungültiger Operand: {operand}")


# Funktionen für Befehle
def execute_instruction(instruction):
    global loop_start, loop_condition  # Diese Zeile nach oben verschieben

    instruction = instruction.split('#')[0].strip()  # Entferne Kommentare und überflüssige Leerzeichen

    if not instruction:
        registers['PC'] += 1
        return

    parts = instruction.replace(',', '').split()
    op = parts[0]

    if op in commands:
        operation = commands[op]["operation"]
        args = parts[1:]  # Die Argumente werden in einer Liste übergeben

        # Debug-Ausgabe, um Labels und Argumente zu überprüfen
        print(f"Executing: {op} with args: {args}")
        print(f"Current labels: {labels}")
        print(f"Current PC: {registers['PC']}")

        # Erstelle eine sichere Ausführungsumgebung
        exec_globals = {
            "get_value": get_value,
            "registers": registers,
            "flags": flags,
            "labels": labels,
            "time": time,
            "display": display,
            "args": args,
            "loop_start": loop_start,
            "loop_condition": loop_condition,
            "execution_halted": False  # Hinzufügen des Halte-Flags
        }

        # Führe den Befehl mit exec aus
        exec(operation, exec_globals)

        # Aktuelle Werte nach exec speichern
        loop_start = exec_globals["loop_start"]
        loop_condition = exec_globals["loop_condition"]

        if exec_globals["execution_halted"]:
            return "HALT"

        if op != 'JMP' and op != 'JEQ':  # Bei Sprungbefehlen nicht automatisch den PC erhöhen
            registers['PC'] += 1
    else:
        raise ValueError(f"Unbekannter Befehl: {op}")


# Programm laden und ausführen
def load_and_run_program(filepath):
    global labels
    with open(filepath, 'r') as f:
        instructions = f.read().strip().splitlines()

    labels = {}
    for i, instr in enumerate(instructions):
        instr_cleaned = instr.split('#')[0].strip()  # Entferne Kommentare
        if instr_cleaned.endswith(':'):
            labels[instr_cleaned[:-1]] = i

    while True:
        instruction = instructions[registers['PC']]
        if instruction.endswith(':'):
            registers['PC'] += 1
            continue
        if execute_instruction(instruction) == 'HALT':
            break


# Warte auf CLI-Eingabe (für INP-Befehl)
def wait_for_cli_input():
    value = input("Eingabe erforderlich: ")
    return int(value)


# Verfügbare Programme auflisten und auswählen
def select_program():
    program_dir = 'programms'
    programs = [f for f in os.listdir(program_dir) if f.endswith('.masm')]

    if not programs:
        print("Keine Programme gefunden.")
        return None

    print("Verfügbare Programme:")
    for i, program in enumerate(programs):
        print(f"{i + 1}: {program}")

    choice = int(input("Wähle ein Programm (Nummer): ")) - 1

    if 0 <= choice < len(programs):
        return os.path.join(program_dir, programs[choice])
    else:
        print("Ungültige Auswahl.")
        return None


# Hauptfunktion
def main():
    program_path = select_program()
    if program_path:
        load_and_run_program(program_path)
        plt.imshow(display, cmap='gray', interpolation='nearest')
        plt.show()


if __name__ == "__main__":
    main()
