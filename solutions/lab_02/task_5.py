import sys
import tracemalloc

# ============================================================
# Часть 1. Размер отдельных объектов
# ============================================================
print("=== Часть 1. Размеры отдельных объектов ===\n")

empty_list = []
list_10 = list(range(10))
tuple_10 = tuple(range(10))
string_10 = "0123456789"
integer = 42
none_obj = None

print(f"Пустой список:          {sys.getsizeof(empty_list)} байт")
print(f"Список из 10 чисел:     {sys.getsizeof(list_10)} байт")
print(f"Кортеж из 10 чисел:     {sys.getsizeof(tuple_10)} байт")
print(f"Строка из 10 символов:  {sys.getsizeof(string_10)} байт")
print(f"Целое число:            {sys.getsizeof(integer)} байт")
print(f"Объект None:            {sys.getsizeof(none_obj)} байт")

print("\nПочему размер контейнера не включает полный размер объектов?")
print("Контейнер (список, кортеж) хранит только ссылки на объекты, а не сами объекты.")
print("Поэтому sys.getsizeof() показывает размер структуры контейнера + массив ссылок,")
print("но не включает размер объектов, на которые эти ссылки указывают.")

# ============================================================
# Часть 2. Рост списка
# ============================================================
print("\n=== Часть 2. Рост списка ===\n")

growing_list = []
prev_size = sys.getsizeof(growing_list)
print(f"Начальный размер: {prev_size} байт (длина: {len(growing_list)})")

for i in range(100):
    growing_list.append(i)
    current_size = sys.getsizeof(growing_list)
    if current_size != prev_size:
        print(f"Длина: {len(growing_list):3d}, размер: {current_size} байт (изменился!)")
        prev_size = current_size

print("\nНаблюдения:")
print("1. Размер списка увеличивается НЕ после каждого append().")
print("2. Python резервирует место с запасом (over-allocation), чтобы не перераспределять")
print("   память при каждом добавлении элемента. Это называется 'geometric growth'.")
print("3. Длина списка — это количество элементов, а размер — это объём выделенной памяти")
print("   под массив ссылок. Размер всегда >= длины.")

# ============================================================
# Часть 3. Измерение через tracemalloc и sys.getsizeof
# ============================================================
print("\n=== Часть 3. Измерение через tracemalloc и sys.getsizeof ===\n")

# Сценарий A: материализованный список
print("Сценарий A: numbers = list(range(100_000))")
tracemalloc.start()
numbers_list = list(range(100_000))
current_a, peak_a = tracemalloc.get_traced_memory()
size_a = sys.getsizeof(numbers_list)
tracemalloc.stop()
del numbers_list

print(f"  tracemalloc — текущий: {current_a / 1024:.2f} КБ, пиковый: {peak_a / 1024:.2f} КБ")
print(f"  sys.getsizeof()      : {size_a / 1024:.2f} КБ (только внешний объект)")

# Сценарий B: объект range (ленивый)
print("\nСценарий B: numbers = range(100_000)")
tracemalloc.start()
numbers_range = range(100_000)
current_b, peak_b = tracemalloc.get_traced_memory()
size_b = sys.getsizeof(numbers_range)
tracemalloc.stop()
del numbers_range

print(f"  tracemalloc — текущий: {current_b / 1024:.2f} КБ, пиковый: {peak_b / 1024:.2f} КБ")
print(f"  sys.getsizeof()      : {size_b} байт")

# Сравнение через sys.getsizeof (это надёжнее)
print(f"\nОтношение размеров (list / range) по sys.getsizeof: {size_a / size_b:.2f}x")
# Вывод: list(range(N)) создаёт все N объектов сразу и тратит много памяти.
#  range(N) — это ленивый объект, который хранит только правило получения значений, а не сами значения.
# Поэтому он занимает минимум памяти.
# Важное замечание:
# tracemalloc показал ~0 КБ для range, потому что range — это C-объект,
# который выделяет память через стандартный malloc, а не через Python-аллокатор.
# tracemalloc отслеживает только аллокации Python-уровня (pymalloc).
# Поэтому для точного измерения размера отдельных объектов лучше использовать sys.getsizeof().
