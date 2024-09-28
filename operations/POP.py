# operations/POP.py

def execute(emulator, operands):
    operand1_type, operand1_value = operands[0]
    operand2_type, operand2_value = operands[1]  # Wird nicht verwendet
    operand3_type, operand3_value = operands[2]  # Wird nicht verwendet

    if operand1_type != 'reg':
        print(f"Thread {emulator.thread_id}: Ungültiger Zieloperand in POP")
        emulator.running = False
        return

    dest = f'R{operand1_value}'
    if emulator.stack:
        emulator.registers[dest] = emulator.stack.pop()
    else:
        print(f"Thread {emulator.thread_id}: Stack unterläuft bei POP")
        emulator.running = False
