# operations/OUT.py

def execute(emulator, operands):
    operand1_type, operand1_value = operands[0]
    operand2_type, operand2_value = operands[1]
    operand3_type, operand3_value = operands[2]  # Wird nicht verwendet

    port = emulator.get_value(operand1_type, operand1_value)
    src = emulator.get_value(operand2_type, operand2_value)
    print(f"Thread {emulator.thread_id}: OUT Port {port}: {src}")
