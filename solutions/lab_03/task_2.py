"""
Базовые алгоритмические схемы: сумма, поиск, подсчёт, сортировка.
Все алгоритмы реализованы вручную — без min(), max(), sum(), sorted().
"""

# ============================================================
# Исходные данные
# ============================================================
measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]

print("Исходные данные:", measurements)
print()

# ============================================================
# Первый проход: сумма, минимум, максимум, чётные
# ============================================================
print("=== Первый проход ===")

total = 0
minimum = measurements[0]
maximum = measurements[0]
even_count = 0

for value in measurements:
    # Сумма
    total += value

    # Минимум
    if value < minimum:
        minimum = value

    # Максимум
    if value > maximum:
        maximum = value

    # Чётные
    if value % 2 == 0:
        even_count += 1

print(f"Сумма: {total}")
print(f"Минимум: {minimum}")
print(f"Максимум: {maximum}")
print(f"Количество чётных: {even_count}")

# ============================================================
# Среднее и второй проход
# ============================================================
mean_value = total / len(measurements)
print(f"\nСреднее значение: {mean_value:.2f}")

# Второй проход: считаем, сколько значений больше среднего
above_mean_count = 0
for value in measurements:
    if value > mean_value:
        above_mean_count += 1

print(f"Значений выше среднего: {above_mean_count}")

# ============================================================
# Линейный поиск первого вхождения
# ============================================================
print("\n=== Линейный поиск ===")

target = int(input("Введите число для поиска: "))

# Прогноз: для 18 ожидаем индекс 3 (первое вхождение),
# для 99 — индекс -1 (отсутствует).

found_index = -1
comparisons_linear = 0

for i in range(len(measurements)):
    comparisons_linear += 1
    if measurements[i] == target:
        found_index = i
        break

print(f"Число {target} найдено на индексе: {found_index}")
print(f"Количество сравнений: {comparisons_linear}")

# ============================================================
# Проверка простоты
# ============================================================
print("\n=== Проверка простоты ===")


def is_prime(n: int) -> bool:
    """Проверяет, является ли число простым.
    Перебирает делители только до sqrt(n) включительно.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Перебираем нечётные делители от 3 до sqrt(n)
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


# Тестовые проверки
test_numbers = [1, 2, 3, 4, 17, 18, 97, 100, 7919]
for num in test_numbers:
    print(f"  {num:>5} — {'простое' if is_prime(num) else 'составное'}")

# ============================================================
# Практическое расширение: сортировка выбором и бинарный поиск
# ============================================================
print("\n=== Практическое расширение ===")


def selection_sort(arr: list) -> tuple[list, int]:
    """Сортировка выбором. Возвращает (отсортированный список, число сравнений)."""
    a = arr.copy()  # не меняем исходный
    n = len(a)
    comparisons = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        # Меняем местами
        a[i], a[min_idx] = a[min_idx], a[i]

    return a, comparisons


def binary_search(arr: list, target: int) -> tuple[int, int]:
    """Бинарный поиск в отсортированном списке.
    Возвращает (индекс или -1, число сравнений).
    """
    left = 0
    right = len(arr) - 1
    comparisons = 0

    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1, comparisons


def linear_search_count(arr: list, target: int) -> tuple[int, int]:
    """Линейный поиск с подсчётом сравнений."""
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons
    return -1, comparisons


# Генератор псевдослучайных данных (детерминированный, без random)
def generate_data(n: int) -> list:
    """Генерирует список из n псевдослучайных чисел."""
    result = []
    seed = 12345
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        result.append(seed % 10000)
    return result


# Тестируем на размерах 10, 100, 1000
sizes = [10, 100, 1000]

print(f"\n{'Размер':<8} {'Сорт. (сравн.)':<18} {'Лин. поиск (сравн.)':<22} {'Бин. поиск (сравн.)':<22}")
print("-" * 70)

for size in sizes:
    data = generate_data(size)
    sorted_data, sort_comparisons = selection_sort(data)

    # Ищем элемент, которого точно нет (худший случай)
    missing_target = -1
    _, linear_comparisons = linear_search_count(sorted_data, missing_target)
    _, binary_comparisons = binary_search(sorted_data, missing_target)

    print(f"{size:<8} {sort_comparisons:<18} {linear_comparisons:<22} {binary_comparisons:<22}")