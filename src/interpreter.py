# interpreter.py
import sys
import struct
import csv

def execute_program(binary_file, memory_range_start, memory_range_end, result_file):
    # Инициализируем память и регистры
    memory = {}
    registers = [0] * 16  # Предполагаем 16 регистров R0 - R15

    # Читаем бинарный файл инструкций
    with open(binary_file, 'rb') as f:
        binary_data = f.read()

    instructions = []
    for i in range(0, len(binary_data), 4):
        instruction = struct.unpack('<I', binary_data[i:i+4])[0]
        instructions.append(instruction)

    # Выполняем инструкции
    pc = 0  # Счетчик команд
    while pc < len(instructions):
        instruction = instructions[pc]
        opcode = instruction & 0x3F
        B = (instruction >> 6) & 0xF

        if opcode == 44:  # LOAD_CONST
            C = (instruction >> 10) & 0x1FFFF
            registers[B] = C
        elif opcode == 14:  # LOAD_MEM
            C = (instruction >> 10) & 0xF
            D = (instruction >> 14) & 0x1FFF
            address = registers[C] + D
            registers[B] = memory.get(address, 0)
        elif opcode == 2:  # STORE_MEM
            C = (instruction >> 10) & 0xF
            address = registers[B]
            memory[address] = registers[C]
        elif opcode == 29:  # ADD
            C = (instruction >> 10) & 0xF
            D = (instruction >> 14) & 0x7FFF
            operand1 = memory.get(D, 0)
            operand2 = registers[C]
            registers[B] = operand1 + operand2
        else:
            raise ValueError(f"Неизвестный опкод: {opcode}")
        pc += 1

    # Извлекаем значения из указанного диапазона памяти
    result_data = []
    for addr in range(memory_range_start, memory_range_end + 1):
        value = memory.get(addr, 0)
        result_data.append({'Address': addr, 'Value': value})

    # Записываем результат в CSV-файл
    with open(result_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['Address', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in result_data:
            writer.writerow(entry)

    print(f"Выполнение завершено. Результаты сохранены в файле: {result_file}")

def main():
    if len(sys.argv) < 5:
        print("Использование: python interpeter.py <binary_file> <memory_range_start> <memory_range_end> <result_file>")
        sys.exit(1)
    binary_file = sys.argv[1]
    memory_range_start = int(sys.argv[2])
    memory_range_end = int(sys.argv[3])
    result_file = sys.argv[4]

    execute_program(binary_file, memory_range_start, memory_range_end, result_file)

if __name__ == '__main__':
    main()
