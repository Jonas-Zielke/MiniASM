# operations/CMP.py

def execute(emulator, operands):
    operand1_type, operand1_value = operands[0]
    operand2_type, operand2_value = operands[1]
    operand3_type, operand3_value = operands[2]  # Wird nicht verwendet

    src1 = emulator.get_value(operand1_type, operand1_value)
    src2 = emulator.get_value(operand2_type, operand2_value)

    emulator.flag_zero = (src1 == src2)
    emulator.flag_greater = (src1 > src2)
    emulator.flag_less = (src1 < src2)
