# main.py

import os
import threading
import time
import importlib.util
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
        self.operations = {}  # Registrierte Operationen

        # Erstelle den geschützten Ordner beim Start des Emulators
        self.create_protected_folder()

        # Lade alle Operationen
        self.load_operations()

    def create_protected_folder(self):
        base_dir = os.path.abspath(os.path.join('programms', self.program_name))
        if not os.path.exists(base_dir):
            try:
                os.makedirs(base_dir, exist_ok=True)
                print(f"Thread {self.thread_id}: Geschützter Ordner '{base_dir}' wurde erstellt.")
            except Exception as e:
                print(f"Thread {self.thread_id}: Fehler beim Erstellen des geschützten Ordners: {e}")
                self.running = False

    def load_operations(self):
        operations_dir = os.path.join(os.path.dirname(__file__), 'operations')
        for filename in os.listdir(operations_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                op_name = filename[:-3]  # Entferne .py
                if op_name in opcodes:
                    filepath = os.path.join(operations_dir, filename)
                    spec = importlib.util.spec_from_file_location(op_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.operations[opcodes[op_name]] = module.execute
                else:
                    print(f"Thread {self.thread_id}: OpCode für Operation '{op_name}' nicht in opcodes.py definiert.")

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
        # Rufe die entsprechende Operation auf
        if opcode in self.operations:
            try:
                self.operations[opcode](self, operands)
                self.instruction_count += 1
            except Exception as e:
                print(f"Thread {self.thread_id}: Fehler bei der Ausführung von Opcode {opcode}: {e}")
                self.running = False
        else:
            print(f"Thread {self.thread_id}: Unbekannter Opcode: {opcode}")
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

    def run(self):
        self.load_program()
        self.start_time = time.time()
        while self.running:
            instr = self.fetch()
            self.decode_execute(instr)
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
