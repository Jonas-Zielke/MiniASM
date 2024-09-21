# main.py

import os
import threading
import time
from opcodes import opcodes

class MiniASMEmulator(threading.Thread):
    def __init__(self, program_data, thread_id, program_name):
        super().__init__()
        self.thread_id = thread_id
        self.program_name = program_name
        self.registers = {f'R{i}': 0 for i in range(8)}
        self.registers.update({'PC': 0, 'SP': 0, 'FLAGS': 0})
        self.memory = bytearray(1024 * 1024)  # 1MB Speicher
        self.stack = []
        self.running = True
        self.program_data = program_data
        self.flag_zero = False  # Zero Flag
        self.flag_greater = False  # Greater Flag
        self.flag_less = False  # Less Flag
        self.instruction_count = 0  # Zähler für ausgeführte Anweisungen
        self.open_files = {}  # Geöffnete Dateien

        # Erstelle den geschützten Ordner beim Start des Emulators
        self.create_protected_folder()

    def create_protected_folder(self):
        base_dir = os.path.abspath(os.path.join('programms', self.program_name))
        if not os.path.exists(base_dir):
            try:
                os.makedirs(base_dir, exist_ok=True)
                print(f"Thread {self.thread_id}: Geschützter Ordner '{base_dir}' wurde erstellt.")
            except Exception as e:
                print(f"Thread {self.thread_id}: Fehler beim Erstellen des geschützten Ordners: {e}")
                self.running = False

    def load_program(self):
        # Lade das Programm in den Speicher ab Adresse 0
        self.memory[:len(self.program_data)] = self.program_data

    def fetch(self):
        if self.registers['PC'] + 8 > len(self.memory):
            self.running = False
            return None
        # Lese 8 Bytes für die Anweisung
        instr_bytes = self.memory[self.registers['PC']:self.registers['PC'] + 8]
        instruction = int.from_bytes(instr_bytes, byteorder='big')
        self.registers['PC'] += 8
        return instruction

    def decode_execute(self, instruction):
        if instruction is None:
            return
        opcode = (instruction >> 56) & 0xFF
        operand1 = (instruction >> 40) & 0xFFFF
        operand2 = (instruction >> 24) & 0xFFFF
        operand3 = (instruction >> 8) & 0xFFFF

        # Opcode zu Anweisung
        opcode_inv = {v: k for k, v in opcodes.items()}
        if opcode not in opcode_inv:
            print(f"Thread {self.thread_id}: Unbekannter Opcode: {opcode}")
            self.running = False
            return

        instr_name = opcode_inv[opcode]

        # Operanden decodieren
        operands = []
        for operand in [operand1, operand2, operand3]:
            if operand & 0x8000:
                # Register operand (höchstes Bit ist 1)
                reg_num = operand & 0x7FFF
                operands.append(('reg', reg_num))
            else:
                # Immediate operand
                # Um Vorzeichen zu berücksichtigen
                imm_value = operand & 0x7FFF
                if imm_value & 0x4000:
                    imm_value -= 0x8000  # Negative Zahl
                operands.append(('imm', imm_value))
        operand1_type, operand1_value = operands[0]
        operand2_type, operand2_value = operands[1]
        operand3_type, operand3_value = operands[2]

        # Implementierung der Anweisungen
        try:
            if instr_name == 'NOP':
                pass

            elif instr_name == 'MOV':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in MOV")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src = self.get_value(operand2_type, operand2_value)
                self.registers[dest] = src

            elif instr_name == 'ADD':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in ADD")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src1 = self.get_value(operand2_type, operand2_value)
                src2 = self.get_value(operand3_type, operand3_value)
                self.registers[dest] = src1 + src2

            elif instr_name == 'SUB':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in SUB")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src1 = self.get_value(operand2_type, operand2_value)
                src2 = self.get_value(operand3_type, operand3_value)
                self.registers[dest] = src1 - src2

            elif instr_name == 'MUL':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in MUL")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src1 = self.get_value(operand2_type, operand2_value)
                src2 = self.get_value(operand3_type, operand3_value)
                self.registers[dest] = src1 * src2

            elif instr_name == 'DIV':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in DIV")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src1 = self.get_value(operand2_type, operand2_value)
                src2 = self.get_value(operand3_type, operand3_value)
                if src2 == 0:
                    print(f"Thread {self.thread_id}: Division durch Null in DIV")
                    self.running = False
                    return
                self.registers[dest] = src1 // src2

            elif instr_name == 'AND':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in AND")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src1 = self.get_value(operand2_type, operand2_value)
                src2 = self.get_value(operand3_type, operand3_value)
                self.registers[dest] = src1 & src2

            elif instr_name == 'OR':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in OR")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src1 = self.get_value(operand2_type, operand2_value)
                src2 = self.get_value(operand3_type, operand3_value)
                self.registers[dest] = src1 | src2

            elif instr_name == 'XOR':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in XOR")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src1 = self.get_value(operand2_type, operand2_value)
                src2 = self.get_value(operand3_type, operand3_value)
                self.registers[dest] = src1 ^ src2

            elif instr_name == 'NOT':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in NOT")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src = self.get_value(operand2_type, operand2_value)
                self.registers[dest] = ~src

            elif instr_name == 'SHL':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in SHL")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src = self.get_value(operand2_type, operand2_value)
                shift = self.get_value(operand3_type, operand3_value)
                self.registers[dest] = src << shift

            elif instr_name == 'SHR':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in SHR")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                src = self.get_value(operand2_type, operand2_value)
                shift = self.get_value(operand3_type, operand3_value)
                self.registers[dest] = src >> shift

            elif instr_name == 'CMP':
                src1 = self.get_value(operand1_type, operand1_value)
                src2 = self.get_value(operand2_type, operand2_value)
                self.flag_zero = (src1 == src2)
                self.flag_greater = (src1 > src2)
                self.flag_less = (src1 < src2)

            elif instr_name == 'JMP':
                addr = self.get_value(operand1_type, operand1_value)
                self.registers['PC'] = addr

            elif instr_name == 'JE':
                addr = self.get_value(operand1_type, operand1_value)
                if self.flag_zero:
                    self.registers['PC'] = addr

            elif instr_name == 'JNE':
                addr = self.get_value(operand1_type, operand1_value)
                if not self.flag_zero:
                    self.registers['PC'] = addr

            elif instr_name == 'JG':
                addr = self.get_value(operand1_type, operand1_value)
                if self.flag_greater:
                    self.registers['PC'] = addr

            elif instr_name == 'JL':
                addr = self.get_value(operand1_type, operand1_value)
                if self.flag_less:
                    self.registers['PC'] = addr

            elif instr_name == 'PUSH':
                src = self.get_value(operand1_type, operand1_value)
                self.stack.append(src)

            elif instr_name == 'POP':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in POP")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                if self.stack:
                    self.registers[dest] = self.stack.pop()
                else:
                    print(f"Thread {self.thread_id}: Stack unterläuft bei POP")
                    self.running = False

            elif instr_name == 'IN':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in IN")
                    self.running = False
                    return
                dest = f'R{operand1_value}'
                port = self.get_value(operand2_type, operand2_value)
                user_input = input(f"Thread {self.thread_id}: IN Port {port}: ")
                try:
                    self.registers[dest] = int(user_input)
                except ValueError:
                    print(f"Thread {self.thread_id}: Ungültige Eingabe.")
                    self.running = False

            elif instr_name == 'OUT':
                port = self.get_value(operand1_type, operand1_value)
                src = self.get_value(operand2_type, operand2_value)
                print(f"Thread {self.thread_id}: OUT Port {port}: {src}")

            elif instr_name == 'PRINT':
                addr = self.get_value(operand1_type, operand1_value)
                length = self.get_value(operand2_type, operand2_value)
                # Lese die Zeichenkette aus dem Speicher
                string_bytes = self.memory[addr:addr + length]
                string = string_bytes.decode('ascii', errors='ignore')
                print(f"Thread {self.thread_id}: {string}")

            # --- Dateioperationen ---
            elif instr_name == 'OPEN':
                filename_addr = self.get_value(operand1_type, operand1_value)
                mode = self.get_value(operand2_type, operand2_value)
                if operand3_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Zieloperand in OPEN")
                    self.running = False
                    return
                fd_reg = f'R{operand3_value}'
                filename = self.read_string_from_memory(filename_addr)
                safe_filename = self.get_safe_path(filename)
                modes = {0: 'r', 1: 'w', 2: 'a'}
                if mode not in modes:
                    print(f"Thread {self.thread_id}: Ungültiger Modus in OPEN")
                    self.running = False
                    return
                try:
                    os.makedirs(os.path.dirname(safe_filename), exist_ok=True)
                    file_obj = open(safe_filename, modes[mode])
                    fd = id(file_obj)  # Verwende die id als Dateideskriptor
                    self.open_files[fd] = file_obj
                    self.registers[fd_reg] = fd
                except Exception as e:
                    print(f"Thread {self.thread_id}: Fehler beim Öffnen der Datei: {e}")
                    self.running = False

            elif instr_name == 'READ':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Dateideskriptor in READ")
                    self.running = False
                    return
                fd_reg = f'R{operand1_value}'
                fd = self.registers.get(fd_reg)
                mem_addr = self.get_value(operand2_type, operand2_value)
                num_bytes = self.get_value(operand3_type, operand3_value)
                if fd in self.open_files:
                    file_obj = self.open_files[fd]
                    data = file_obj.read(num_bytes)
                    self.memory[mem_addr:mem_addr+len(data)] = data.encode('utf-8')
                else:
                    print(f"Thread {self.thread_id}: Ungültiger Dateideskriptor in READ")
                    self.running = False

            elif instr_name == 'WRITE':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Dateideskriptor in WRITE")
                    self.running = False
                    return
                fd_reg = f'R{operand1_value}'
                fd = self.registers.get(fd_reg)
                mem_addr = self.get_value(operand2_type, operand2_value)
                num_bytes = self.get_value(operand3_type, operand3_value)
                if fd in self.open_files:
                    file_obj = self.open_files[fd]
                    data = self.memory[mem_addr:mem_addr+num_bytes].decode('utf-8', errors='ignore')
                    file_obj.write(data)
                else:
                    print(f"Thread {self.thread_id}: Ungültiger Dateideskriptor in WRITE")
                    self.running = False

            elif instr_name == 'CLOSE':
                if operand1_type != 'reg':
                    print(f"Thread {self.thread_id}: Ungültiger Dateideskriptor in CLOSE")
                    self.running = False
                    return
                fd_reg = f'R{operand1_value}'
                fd = self.registers.get(fd_reg)
                if fd in self.open_files:
                    file_obj = self.open_files.pop(fd)
                    file_obj.close()
                else:
                    print(f"Thread {self.thread_id}: Ungültiger Dateideskriptor in CLOSE")
                    self.running = False

            elif instr_name == 'HALT':
                self.running = False

            else:
                print(f"Thread {self.thread_id}: Anweisung '{instr_name}' nicht implementiert.")
                self.running = False

        except Exception as e:
            print(f"Thread {self.thread_id}: Fehler bei der Ausführung von '{instr_name}': {e}")
            self.running = False

    def get_value(self, operand_type, operand_value):
        if operand_type == 'reg':
            return self.registers.get(f'R{operand_value}', 0)
        else:
            return operand_value

    def read_string_from_memory(self, addr):
        string_bytes = bytearray()
        while True:
            byte = self.memory[addr]
            if byte == 0:
                break
            string_bytes.append(byte)
            addr += 1
        return string_bytes.decode('utf-8', errors='ignore')

    def get_safe_path(self, filename):
        base_dir = os.path.abspath(os.path.join('programms', self.program_name))
        safe_path = os.path.normpath(os.path.join(base_dir, filename))
        if not safe_path.startswith(base_dir):
            raise ValueError("Unsichere Dateipfadoperation verhindert.")
        return safe_path

    def run(self):
        self.load_program()
        self.start_time = time.time()
        while self.running:
            instr = self.fetch()
            self.decode_execute(instr)
            self.instruction_count += 1
        self.end_time = time.time()
        execution_time = self.end_time - self.start_time
        print(f"Thread {self.thread_id}: Programm beendet.")
        print(f"Thread {self.thread_id}: Ausführungszeit: {execution_time:.6f} Sekunden")
        print(f"Thread {self.thread_id}: Ausgeführte Anweisungen: {self.instruction_count}")
        print(f"Thread {self.thread_id}: Registerzustand nach Programmende:")
        for reg, val in self.registers.items():
            print(f"{reg}: {val}")
        print("\n")

def main():
    programms_dir = 'programms'
    if not os.path.exists(programms_dir):
        try:
            os.makedirs(programms_dir, exist_ok=True)
            print(f"Verzeichnis '{programms_dir}' wurde erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen des Verzeichnisses '{programms_dir}': {e}")
            return
    programms = [f for f in os.listdir(programms_dir) if f.endswith('.bin')]

    if not programms:
        print("Keine Programme gefunden. Bitte assemblieren Sie zuerst ein Programm.")
        return

    print("Verfügbare Programme:")
    for idx, prog in enumerate(programms):
        print(f"{idx + 1}: {prog}")

    choices = input("Welche Programme möchten Sie ausführen? (Geben Sie die Nummern mit Komma getrennt ein, max. 4): ")
    choices = choices.replace(' ', '').split(',')
    if len(choices) > 4:
        print("Sie können maximal 4 Programme gleichzeitig ausführen.")
        return

    threads = []
    for choice in choices:
        if not choice.isdigit():
            print(f"Ungültige Auswahl: {choice}")
            continue
        idx = int(choice) - 1
        if idx < 0 or idx >= len(programms):
            print(f"Ungültige Auswahl: {choice}")
            continue

        program_path = os.path.join(programms_dir, programms[idx])
        try:
            with open(program_path, 'rb') as f:
                program_data = f.read()
        except Exception as e:
            print(f"Fehler beim Lesen der Datei '{programms[idx]}': {e}")
            continue

        program_name = os.path.splitext(programms[idx])[0]
        emulator = MiniASMEmulator(program_data, thread_id=choice, program_name=program_name)
        threads.append(emulator)

    # Threads starten
    for thread in threads:
        thread.start()

    # Auf Threads warten
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
