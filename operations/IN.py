# operations/IN.py

def execute(emulator, operands):
    operand1_type, operand1_value = operands[0]
    operand2_type, operand2_value = operands[1]
    operand3_type, operand3_value = operands[2]  # Wird nicht verwendet

    if operand1_type != 'reg':
        print(f"Thread {emulator.thread_id}: Ungültiger Zieloperand in IN")
        emulator.running = False
        return

    dest = f'R{operand1_value}'
    port = emulator.get_value(operand2_type, operand2_value)
    user_input = input(f"Thread {emulator.thread_id}: IN Port {port}: ")
    try:
        emulator.registers[dest] = int(user_input)
    except ValueError:
        print(f"Thread {emulator.thread_id}: Ungültige Eingabe.")
        emulator.running = False
