"""
Функции, параметры и области видимости.
Демонстрация LEGB, замыканий и типичных ловушек Python.
"""


# ============================================================
# 1. Четыре функции из задания
# ============================================================

def arithmetic_mean(values: list[float]) -> float:
    """Возвращает среднее арифметическое непустого списка.

    Контракт:
    - Вход: непустой список чисел.
    - Выход: float — среднее значение.
    - Особый случай: пустой список → ValueError.
    """
    if not values:
        raise ValueError("Список не должен быть пустым")
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def normalize_name(name: str) -> str:
    """Удаляет лишние пробелы и приводит каждую часть имени к нужному регистру.

    Контракт:
    - Вход: строка с именем (возможно, с лишними пробелами).
    - Выход: строка вида "Имя Фамилия" (каждая часть с заглавной буквы).
    - Особый случай: пустая строка → пустая строка.
    """
    if not name or not name.strip():
        return ""
    parts = name.split()
    return " ".join(part.capitalize() for part in parts)


def build_report(
        student: str,
        results: list[int],
        *,
        precision: int = 2,
        prefix: str = "Результат",
) -> str:
    """Формирует строковый отчёт о результатах студента.

    Контракт:
    - Вход: имя студента, список результатов, точность и префикс (только по имени).
    - Выход: строка вида "Результат <student>: <среднее> (N оценок)".
    - precision и prefix — keyword-only параметры.
    """
    mean = arithmetic_mean(results)
    return f"{prefix} {student}: {mean:.{precision}f} ({len(results)} оценок)"


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Возвращает очищенные теги без пустых значений и повторов.

    Контракт:
    - Вход: произвольное число строк-тегов + флаг lowercase.
    - Выход: кортеж уникальных тегов.
    - Пустые строки и пробельные теги отбрасываются.
    """
    seen = set()
    result = []
    for tag in tags:
        cleaned = tag.strip()
        if not cleaned:
            continue
        if lowercase:
            cleaned = cleaned.lower()
        if cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return tuple(result)


# ============================================================
# Проверки через assert
# ============================================================

print("=== Проверки функций ===\n")

# arithmetic_mean
assert arithmetic_mean([1, 2, 3]) == 2.0
assert arithmetic_mean([10]) == 10.0
assert abs(arithmetic_mean([1.5, 2.5]) - 2.0) < 1e-9
print("✓ arithmetic_mean: все assert прошли")

# normalize_name
assert normalize_name("  anna   smirnova  ") == "Anna Smirnova"
assert normalize_name("python") == "Python"
assert normalize_name("") == ""
assert normalize_name("   ") == ""
print("✓ normalize_name: все assert прошли")

# build_report
assert build_report("Анна", [80, 90, 100]) == "Результат Анна: 90.00 (3 оценок)"
assert build_report("Борис", [50], precision=0) == "Результат Борис: 50 (1 оценок)"
assert build_report("Дарья", [100], prefix="Оценка") == "Оценка Дарья: 100.00 (1 оценок)"
print("✓ build_report: все assert прошли")

# collect_tags
assert collect_tags("Python", "python", "  ") == ("python",)
assert collect_tags("A", "B", "A", lowercase=False) == ("A", "B")
assert collect_tags() == ()
print("✓ collect_tags: все assert прошли")

# ============================================================
# Демонстрация распаковки * и **
# ============================================================

print("\n=== Распаковка аргументов ===\n")

# Распаковка списка через *
scores = [85, 90, 95]
print(f"collect_tags(*['Py', 'JS', 'Py']): {collect_tags(*['Py', 'JS', 'Py'])}")

# Распаковка словаря через **
params = {"student": "Анна", "results": [80, 90, 100], "precision": 1, "prefix": "Итог"}
print(f"build_report(**params): {build_report(**params)}")

# ============================================================
# Исследование LEGB
# ============================================================

print("\n=== LEGB и nonlocal ===\n")

course = "Python"  # глобальное имя


def outer():
    course = "Алгоритмы"  # имя в объемлющей области (enclosing)

    def inner():
        nonlocal course  # ссылаемся на enclosing, не на global
        course = "Машинное обучение"
        print(f"  inner: course = {course!r}")

    print(f"  outer до inner: course = {course!r}")
    inner()
    print(f"  outer после inner: course = {course!r}")


print(f"Глобально: course = {course!r}")
outer()
print(f"Глобально после outer: course = {course!r}")
print("(глобальное имя не изменилось — nonlocal затронул только enclosing)")

# ============================================================
# Ошибка изменяемого значения по умолчанию
# ============================================================

print("\n=== Ошибка изменяемого значения по умолчанию ===\n")


def add_result_buggy(value, results=[]):
    """ОШИБКА: results — общий для всех вызовов!"""
    results.append(value)
    return results


print("Вызовы add_result_buggy:")
print(f"  1-й вызов (5):   {add_result_buggy(5)}")
print(f"  2-й вызов (10):  {add_result_buggy(10)}")
print(f"  3-й вызов (15):  {add_result_buggy(15)}")
print("⚠️ Список накапливает значения между вызовами — это баг!")


def add_result_fixed(value, results=None):
    """Правильный вариант: None как сигнал 'создать новый список'."""
    if results is None:
        results = []
    results.append(value)
    return results


print("\nВызовы add_result_fixed:")
print(f"  1-й вызов (5):   {add_result_fixed(5)}")
print(f"  2-й вызов (10):  {add_result_fixed(10)}")
print(f"  3-й вызов (15):  {add_result_fixed(15)}")
print("✓ Каждый вызов работает с новым списком")

# ============================================================
# Практическое расширение: apply_to_results и замыкания
# ============================================================

print("\n=== Практическое расширение ===\n")


def apply_to_results(operation, values):
    """Применяет операцию ко всем значениям и возвращает список результатов."""
    return [operation(v) for v in values]


def make_threshold_checker(threshold):
    """Фабрика функций: возвращает проверку 'значение >= threshold'."""

    def checker(value):
        return value >= threshold

    return checker


scores = [45, 72, 88, 95, 60, 30]


# Именованная функция
def double(x):
    return x * 2


print(f"apply_to_results(double, {scores}):")
print(f"  {apply_to_results(double, scores)}")

# Lambda
print(f"\napply_to_results(lambda x: x + 10, {scores}):")
print(f"  {apply_to_results(lambda x: x + 10, scores)}")

# Фабрика функций
check_passed = make_threshold_checker(60)
check_excellent = make_threshold_checker(90)

print(f"\ncheck_passed(75) = {check_passed(75)}")
print(f"check_passed(55) = {check_passed(55)}")
print(f"check_excellent(95) = {check_excellent(95)}")
print(f"check_excellent(85) = {check_excellent(85)}")

# Фильтрация через замыкание
passed = [s for s in scores if check_passed(s)]
print(f"\nСтуденты, сдавшие на >= 60: {passed}")

# ============================================================
# Демонстрация замыкания
# ============================================================

print("\n=== Что сохраняется в замыкании? ===\n")

checker_50 = make_threshold_checker(50)
checker_80 = make_threshold_checker(80)

print(f"checker_50.__closure__: {checker_50.__closure__}")
print(f"checker_80.__closure__: {checker_80.__closure__}")
print("Каждая функция хранит своё значение threshold в замыкании.")
print("Это разные объекты, поэтому пороги независимы.")