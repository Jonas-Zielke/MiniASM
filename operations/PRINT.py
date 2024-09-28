# operations/PRINT.py

def execute(emulator, operands):
    operand1_type, operand1_value = operands[0]
    operand2_type, operand2_value = operands[1]
    operand3_type, operand3_value = operands[2]  # Wird nicht verwendet

    addr = emulator.get_value(operand1_type, operand1_value)
    length = emulator.get_value(operand2_type, operand2_value)

    # Lese die Zeichenkette aus dem Speicher
    string_bytes = emulator.memory[addr:addr + length]
    try:
        string = string_bytes.decode('ascii')
    except UnicodeDecodeError:
        string = string_bytes.decode('ascii', errors='ignore')
    print(f"Thread {emulator.thread_id}: {string}")
