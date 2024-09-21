# converter.py

import os
from opcodes import opcodes

def assemble_instruction(line, labels, current_address, pass_num, instructions):
    # Kommentare entfernen und Leerzeichen bereinigen
    line = line.split(';')[0].strip()
    if not line:
        return None, current_address

    # Initialisiere Label
    label = None

    # Überprüfe, ob die Zeile ein Label enthält
    while ':' in line:
        parts = line.split(':', 1)
        label = parts[0].strip()
        line = parts[1].strip()
        # Speichere das Label mit der aktuellen Adresse
        if pass_num == 1:
            labels[label] = current_address

    if not line:
        return None, current_address

    parts = line.replace(',', ' ').split()
    if not parts:
        return None, current_address

    instruction = parts[0].upper()
    operands = parts[1:] if len(parts) > 1 else []

    if instruction == 'DB':
        data_bytes = []
        data_line = ' '.join(operands)
        idx = 0
        while idx < len(data_line):
            if data_line[idx] == "'":
                # String finden
                end_idx = data_line.find("'", idx + 1)
                if end_idx == -1:
                    raise ValueError("Unvollständiger String in DB")
                string = data_line[idx + 1:end_idx]
                data_bytes.extend([ord(c) for c in string])
                idx = end_idx + 1
            elif data_line[idx].isdigit() or (data_line[idx] == '-' and data_line[idx + 1].isdigit()):
                # Zahl finden
                end_idx = idx
                while end_idx < len(data_line) and (data_line[end_idx].isdigit() or data_line[end_idx] == '-'):
                    end_idx += 1
                number = int(data_line[idx:end_idx])
                data_bytes.append(number & 0xFF)
                idx = end_idx
            elif data_line[idx] == ',' or data_line[idx] == ' ':
                idx += 1
            else:
                raise ValueError(f"Ungültiger Datenwert in DB: {data_line[idx]}")
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
        if operand.upper().startswith('R'):
            # Register Operand
            value = ('reg', int(operand[1:]))
        elif operand.startswith('#'):
            # Unmittelbarer Wert
            value = ('imm', int(operand[1:]))
        elif operand.startswith("'") and operand.endswith("'"):
            # String-Operand (für Dateioperationen)
            value = operand[1:-1]
        elif operand.startswith('0X'):
            # Hexadezimaler Wert
            value = ('imm', int(operand, 16))
        elif operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
            # Unmittelbarer Wert
            value = ('imm', int(operand))
        else:
            # Label (wird im zweiten Durchlauf aufgelöst)
            value = operand
        operand_values.append(value)

    # Padding auf 3 Operanden
    while len(operand_values) < 3:
        operand_values.append(('imm', 0))

    if pass_num == 1:
        current_address += 6  # Jede Anweisung ist 6 Bytes lang
        return None, current_address
    else:
        # Operanden auflösen
        resolved_operands = []
        for op in operand_values:
            if isinstance(op, tuple):
                operand_type, operand_value = op
                if operand_type == 'reg':
                    resolved_operands.append((operand_type, operand_value))
                elif operand_type == 'imm':
                    resolved_operands.append((operand_type, operand_value))
            elif isinstance(op, str):
                # String-Literals oder Labels
                if op in labels:
                    resolved_operands.append(('imm', labels[op]))
                else:
                    # String-Literals für Dateioperationen
                    # Schreibe den String in den Speicher und verwende die Adresse
                    string_bytes = op.encode('utf-8') + b'\x00'  # Nullterminierung
                    op_address = current_address
                    resolved_operands.append(('imm', op_address))
                    current_address += len(string_bytes)
                    instructions.append(('DB', string_bytes))
            else:
                # Sollte nicht passieren
                resolved_operands.append(('imm', op))

        # Speichere die Anweisung
        instructions.append((opcode, resolved_operands))
        current_address += 6
        return None, current_address

def main():
    asm_path = input("Bitte geben Sie den Pfad zur Assembly-Datei ein: ")
    if not os.path.isfile(asm_path):
        print("Datei nicht gefunden.")
        return

    output_filename = os.path.basename(asm_path).rsplit('.', 1)[0] + '.bin'
    output_path = os.path.join('programms', output_filename)

    # Labels sammeln
    labels = {}
    instructions = []
    current_address = 0

    with open(asm_path, 'r') as asm_file:
        lines = asm_file.readlines()

    # Erster Durchlauf: Labels sammeln und Adressen berechnen
    current_address = 0
    for line in lines:
        _, current_address = assemble_instruction(line, labels, current_address, pass_num=1, instructions=instructions)

    # Zweiter Durchlauf: Anweisungen assemblieren
    current_address = 0
    instructions = []
    for line in lines:
        _, current_address = assemble_instruction(line, labels, current_address, pass_num=2, instructions=instructions)

    # Schreibe die Anweisungen in die Binärdatei
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
                instruction_value = opcode << 40
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
                        instruction_value |= (operand_value & 0xFFFF) << 24
                    elif i == 1:
                        instruction_value |= (operand_value & 0xFFFF) << 8
                    elif i == 2:
                        instruction_value |= (operand_value & 0xFF)
                bin_file.write(instruction_value.to_bytes(6, byteorder='big'))

    print(f"Das Programm wurde erfolgreich in '{output_path}' gespeichert.")
    print("Labels und Adressen:")
    for label, addr in labels.items():
        print(f"{label}: {addr}")

if __name__ == "__main__":
    main()
