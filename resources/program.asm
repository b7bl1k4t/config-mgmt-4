# Инициализация константы 1 в памяти по адресу 1
LOAD_CONST R1, 1       # R1 = 1
LOAD_CONST R2, 1       # R2 = 1 (адрес 1)
STORE_MEM R2, R1       # Сохранить R1 в memory[1]

# Инициализация вектора длины 4 по адресам 100-103
LOAD_CONST R0, 100     # R0 = 100 (адрес вектора)
LOAD_CONST R1, 10      # R1 = 10 (первый элемент)
STORE_MEM R0, R1       # memory[100] = 10

ADD R0, R0, 1          # R0 = R0 + memory[1] (увеличиваем адрес на 1)
LOAD_CONST R1, 20
STORE_MEM R0, R1       # memory[101] = 20

ADD R0, R0, 1          # R0 = R0 + memory[1]
LOAD_CONST R1, 30
STORE_MEM R0, R1       # memory[102] = 30

ADD R0, R0, 1          # R0 = R0 + memory[1]
LOAD_CONST R1, 40
STORE_MEM R0, R1       # memory[103] = 40

# Сброс R0 к начальному адресу вектора
LOAD_CONST R0, 100     # R0 = 100

# Загрузка константы 12 в R1
LOAD_CONST R1, 12      # R1 = 12

# Инициализация адреса для результата
LOAD_CONST R3, 200     # R3 = 200 (начальный адрес для результатов)

# Инициализация счетчика цикла в R2
LOAD_CONST R2, 0       # R2 = 0 (счетчик итераций)

# Инициализация константы 4 в R4 (размер вектора)
LOAD_CONST R4, 4       # R4 = 4

# Инициализация константы 1 в R5
LOAD_CONST R5, 1       # R5 = 1

# Метка начала цикла (эмулируем цикл вручную из-за отсутствия переходов)

LOAD_CONST R1, 12
LOAD_CONST R2, 2
STORE_MEM R2, R1

# Первая итерация
LOAD_MEM R6, R0, 0     # R6 = memory[R0 + 0]
ADD R7, R6, 2         # R7 = R6 + 12
STORE_MEM R3, R7       # memory[R3] = R7 (сохранение результата)
ADD R0, R0, 1          # R0 = R0 + memory[1] (увеличиваем адрес исходного вектора)
ADD R3, R3, 1          # R3 = R3 + memory[1] (увеличиваем адрес результата)

# Вторая итерация
LOAD_MEM R6, R0, 0
ADD R7, R6, 2
STORE_MEM R3, R7
ADD R0, R0, 1
ADD R3, R3, 1

# Третья итерация
LOAD_MEM R6, R0, 0
ADD R7, R6, 2
STORE_MEM R3, R7
ADD R0, R0, 1
ADD R3, R3, 1

# Четвертая итерация
LOAD_MEM R6, R0, 0
ADD R7, R6, 2
STORE_MEM R3, R7
# Цикл завершен

# Программа завершена
