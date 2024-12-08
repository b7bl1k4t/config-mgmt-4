# assembler.py
import sys
import csv
import struct

# Определяем опкоды для инструкций
OPCODES = {
    'LOAD_CONST': 44,
    'LOAD_MEM': 14,
    'STORE_MEM': 2,
    'ADD': 29
}

def parse_line(line):
    # Удаляем комментарии и лишние пробелы
    line = line.split('#')[0].strip()
    if not line:
        return None
    tokens = line.replace(',', '').split()
    return tokens

def assemble_instruction(tokens):
    mnemonic = tokens[0]
    opcode = OPCODES.get(mnemonic)
    if opcode is None:
        raise ValueError(f"Неизвестная инструкция: {mnemonic}")
    if mnemonic == 'LOAD_CONST':
        _, reg_str, const_str = tokens
        B = int(reg_str.replace('R', ''))
        C = int(const_str)
        instruction = (opcode & 0x3F)  # A: биты 0-5
        instruction |= (B & 0xF) << 6  # B: биты 6-9
        instruction |= (C & 0x1FFFF) << 10  # C: биты 10-26
    elif mnemonic == 'LOAD_MEM':
        _, reg_dest_str, reg_base_str, offset_str = tokens
        B = int(reg_dest_str.replace('R', ''))
        C = int(reg_base_str.replace('R', ''))
        D = int(offset_str)
        instruction = (opcode & 0x3F)  # A: биты 0-5
        instruction |= (B & 0xF) << 6  # B: биты 6-9
        instruction |= (C & 0xF) << 10  # C: биты 10-13
        instruction |= (D & 0x1FFF) << 14  # D: биты 14-26
    elif mnemonic == 'STORE_MEM':
        _, reg_addr_str, reg_value_str = tokens
        B = int(reg_addr_str.replace('R', ''))
        C = int(reg_value_str.replace('R', ''))
        instruction = (opcode & 0x3F)  # A: биты 0-5
        instruction |= (B & 0xF) << 6  # B: биты 6-9
        instruction |= (C & 0xF) << 10  # C: биты 10-13
    elif mnemonic == 'ADD':
        _, reg_dest_str, reg_src_str, addr_str = tokens
        B = int(reg_dest_str.replace('R', ''))
        C = int(reg_src_str.replace('R', ''))
        D = int(addr_str)
        instruction = (opcode & 0x3F)  # A: биты 0-5
        instruction |= (B & 0xF) << 6  # B: биты 6-9
        instruction |= (C & 0xF) << 10  # C: биты 10-13
        instruction |= (D & 0x7FFF) << 14  # D: биты 14-28
    else:
        raise ValueError(f"Неизвестная инструкция: {mnemonic}")
    return instruction

def main():
    if len(sys.argv) < 4:
        print("Использование: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    instructions = []
    log_data = []

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        for line_num, line in enumerate(f, 1):
            tokens = parse_line(line)
            if tokens is None:
                continue
            try:
                instruction = assemble_instruction(tokens)
                instructions.append(instruction)
                log_entry = {'Line': line_num, 'Instruction': line.strip(), 'Opcode': instruction}
                log_data.append(log_entry)
            except ValueError as e:
                print(f"Ошибка в строке {line_num}: {e}")
                sys.exit(1)

    # Записываем бинарный файл
    with open(output_file, 'wb' ) as f:
        for instr in instructions:
            f.write(struct.pack('<I', instr))

    # Записываем лог-файл в формате CSV
    with open(log_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['Line', 'Instruction', 'Opcode']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in log_data:
            writer.writerow(entry)

    print(f"Ассемблирование завершено. Бинарный файл: {output_file}, Лог-файл: {log_file}")

if __name__ == '__main__':
    main()
