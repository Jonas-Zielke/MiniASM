# operations/JMP.py

def execute(emulator, operands):
    operand1_type, operand1_value = operands[0]
    operand2_type, operand2_value = operands[1]  # Wird nicht verwendet
    operand3_type, operand3_value = operands[2]  # Wird nicht verwendet

    addr = emulator.get_value(operand1_type, operand1_value)
    emulator.registers['PC'] = addr
