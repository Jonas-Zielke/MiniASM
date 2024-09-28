# operations/NOT.py

def execute(emulator, operands):
    operand1_type, operand1_value = operands[0]
    operand2_type, operand2_value = operands[1]
    operand3_type, operand3_value = operands[2]

    if operand1_type != 'reg':
        print(f"Thread {emulator.thread_id}: Ungültiger Zieloperand in NOT")
        emulator.running = False
        return

    dest = f'R{operand1_value}'
    src = emulator.get_value(operand2_type, operand2_value)
    emulator.registers[dest] = ~src
