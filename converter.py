# converter.py

import os
import shlex
from opcodes import opcodes

def assemble_instruction(line, labels, current_address, pass_num, instructions):
    # Kommentare entfernen und Leerzeichen bereinigen
    line = line.split(';')[0].strip()
    if not line:
        return None, current_address

    # Überprüfe, ob die Zeile ein Label enthält
    while ':' in line:
        parts = line.split(':', 1)
        label = parts[0].strip()
        line = parts[1].strip()
        # Speichere das Label mit der aktuellen Adresse
        if pass_num == 1:
            if label in labels:
                raise ValueError(f"Label '{label}' mehrfach definiert.")
            labels[label] = current_address

    if not line:
        return None, current_address

    # Ersetze Kommas durch Leerzeichen, um Operanden zu trennen
    try:
        parts = shlex.split(line)
    except ValueError as e:
        raise ValueError(f"Fehler beim Parsen der Zeile: {line}\n{e}")

    # Entferne unnötige Kommas aus den Tokens
    parts = [token.rstrip(',') for token in parts if token != ',']

    if not parts:
        return None, current_address

    instruction = parts[0].upper()
    operands = parts[1:] if len(parts) > 1 else []

    if instruction == 'DB':
        data_bytes = []
        for operand in operands:
            # Versuche, den Operand als Zahl zu interpretieren
            if operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
                number = int(operand)
                data_bytes.append(number & 0xFF)
            else:
                # Behandle den Operand als String
                string = operand
                data_bytes.extend([ord(c) for c in string])
                data_bytes.append(0)  # Nullterminierung
        if pass_num == 1:
            current_address += len(data_bytes)
            return None, current_address
        else:
            instructions.append(('DB', data_bytes))
            current_address += len(data_bytes)
            return None, current_address

    if instruction not in opcodes:
        raise ValueError(f"Unbekannte Anweisung: {instruction}")

    opcode = opcodes[instruction]
    operand_values = []

    for operand in operands:
        operand = operand.strip()
        if operand.upper().startswith('R') and operand[1:].isdigit():
            # Register Operand
            value = ('reg', int(operand[1:]))
        elif operand.startswith('#') and (operand[1:].isdigit() or (operand[1] == '-' and operand[2:].isdigit())):
            # Unmittelbarer Wert
            value = ('imm', int(operand[1:]))
        elif operand.startswith("'") and operand.endswith("'"):
            # String-Literal (für Dateioperationen)
            value = operand[1:-1]
        elif operand.upper().startswith('0X') and len(operand) > 2:
            # Hexadezimaler Wert
            try:
                value = ('imm', int(operand, 16))
            except ValueError:
                raise ValueError(f"Ungültiger hexadezimaler Wert: {operand}")
        elif operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
            # Unmittelbarer Wert ohne #
            value = ('imm', int(operand))
        else:
            # Label (wird im zweiten Durchlauf aufgelöst)
            value = ('label', operand)
        operand_values.append(value)

    # Padding auf 3 Operanden
    while len(operand_values) < 3:
        operand_values.append(('imm', 0))

    if pass_num == 1:
        current_address += 8  # Jede Anweisung ist jetzt 8 Bytes lang
        return None, current_address
    else:
        # Operanden auflösen
        resolved_operands = []
        for op in operand_values:
            operand_type, operand_value = op
            if operand_type == 'reg':
                resolved_operands.append((operand_type, operand_value))
            elif operand_type == 'imm':
                resolved_operands.append((operand_type, operand_value))
            elif operand_type == 'label':
                if operand_value in labels:
                    resolved_operands.append(('imm', labels[operand_value]))
                else:
                    raise ValueError(f"Undefiniertes Label: {operand_value}")
            else:
                # String-Literal
                string_bytes = operand_value.encode('utf-8') + b'\x00'  # Nullterminierung
                op_address = current_address
                resolved_operands.append(('imm', op_address))
                current_address += len(string_bytes)
                instructions.append(('DB', list(string_bytes)))

        # Speichere die Anweisung
        instructions.append((opcode, resolved_operands))
        current_address += 8
        return None, current_address

def main():
    asm_path = input("Bitte geben Sie den Pfad zur Assembly-Datei ein: ")
    if not os.path.isfile(asm_path):
        print("Datei nicht gefunden.")
        return

    # Stelle sicher, dass das Verzeichnis 'programms' existiert
    output_dir = 'programms'
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Verzeichnis '{output_dir}' wurde erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen des Verzeichnisses '{output_dir}': {e}")
            return

    output_filename = os.path.basename(asm_path).rsplit('.', 1)[0] + '.bin'
    output_path = os.path.join(output_dir, output_filename)

    # Labels sammeln
    labels = {}
    current_address = 0

    with open(asm_path, 'r') as asm_file:
        lines = asm_file.readlines()

    # Erster Durchlauf: Labels sammeln und Adressen berechnen
    for line in lines:
        try:
            _, current_address = assemble_instruction(line, labels, current_address, pass_num=1, instructions=[])
        except ValueError as ve:
            print(f"Fehler im ersten Durchlauf: {ve}")
            return

    # Zweiter Durchlauf: Anweisungen assemblieren
    current_address = 0
    instructions = []
    for line in lines:
        try:
            _, current_address = assemble_instruction(line, labels, current_address, pass_num=2, instructions=instructions)
        except ValueError as ve:
            print(f"Fehler im zweiten Durchlauf: {ve}")
            return

    # Schreibe die Anweisungen in die Binärdatei
    try:
        with open(output_path, 'wb') as bin_file:
            for instr_or_data in instructions:
                if instr_or_data[0] == 'DB':
                    # Daten schreiben
                    data_bytes = instr_or_data[1]
                    bin_file.write(bytes(data_bytes))
                else:
                    opcode = instr_or_data[0]
                    operands = instr_or_data[1]
                    # Maschineninstruktion erstellen
                    instruction_value = opcode << 56
                    for i, operand in enumerate(operands):
                        operand_type, operand_value = operand
                        if operand_type == 'reg':
                            # Setze das höchste Bit, um anzuzeigen, dass es sich um ein Register handelt
                            operand_value = operand_value | 0x8000
                        else:
                            # Unmittelbarer Wert, höchstes Bit ist 0
                            operand_value = operand_value & 0x7FFF

                        # Position bestimmen
                        if i == 0:
                            instruction_value |= (operand_value & 0xFFFF) << 40
                        elif i == 1:
                            instruction_value |= (operand_value & 0xFFFF) << 24
                        elif i == 2:
                            instruction_value |= (operand_value & 0xFFFF) << 8
                    bin_file.write(instruction_value.to_bytes(8, byteorder='big'))
    except Exception as e:
        print(f"Fehler beim Schreiben der Binärdatei: {e}")
        return

    print(f"Das Programm wurde erfolgreich in '{output_path}' gespeichert.")
    print("Labels und Adressen:")
    for label, addr in labels.items():
        print(f"{label}: {addr}")

if __name__ == "__main__":
    main()
