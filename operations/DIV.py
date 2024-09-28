# operations/DIV.py

def execute(emulator, operands):
    operand1_type, operand1_value = operands[0]
    operand2_type, operand2_value = operands[1]
    operand3_type, operand3_value = operands[2]

    if operand1_type != 'reg':
        print(f"Thread {emulator.thread_id}: Ungültiger Zieloperand in DIV")
        emulator.running = False
        return

    dest = f'R{operand1_value}'
    src1 = emulator.get_value(operand2_type, operand2_value)
    src2 = emulator.get_value(operand3_type, operand3_value)

    if src2 == 0:
        print(f"Thread {emulator.thread_id}: Division durch Null in DIV")
        emulator.running = False
        return

    emulator.registers[dest] = src1 // src2
