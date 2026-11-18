"""
Анализатор учебных результатов.
Программа анализирует успеваемость группы студентов:
считает статистику по каждому студенту и по группе в целом,
находит лидеров, формирует текстовый отчёт.
"""

# ============================================================
# Исходные данные
# ============================================================
students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}


# ============================================================
# Базовые функции (без min/max/sum)
# ============================================================

def mean(values: list[float]) -> float:
    """Среднее арифметическое непустого списка чисел.

    Контракт:
    - Вход: список чисел (непустой).
    - Выход: float — среднее значение.
    - Особый случай: пустой список → ValueError.
    """
    if not values:
        raise ValueError("mean() требует непустой список")
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def minimum(values: list) -> float:
    """Минимум списка без использования min().

    Контракт:
    - Вход: непустой список сравнимых элементов.
    - Выход: минимальный элемент.
    - Особый случай: пустой список → ValueError.
    """
    if not values:
        raise ValueError("minimum() требует непустой список")
    result = values[0]
    for v in values[1:]:
        if v < result:
            result = v
    return result


def maximum(values: list) -> float:
    """Максимум списка без использования max().

    Контракт:
    - Вход: непустой список сравнимых элементов.
    - Выход: максимальный элемент.
    - Особый случай: пустой список → ValueError.
    """
    if not values:
        raise ValueError("maximum() требует непустой список")
    result = values[0]
    for v in values[1:]:
        if v > result:
            result = v
    return result


def classify(score: float) -> str:
    """Классифицирует средний балл в текстовую категорию.

    Контракт:
    - Вход: число от 0 до 100.
    - Выход: строка — название категории.
    - Особый случай: значение вне [0, 100] → "некорректный балл".
    """
    if score < 0 or score > 100:
        return "некорректный балл"
    if score >= 90:
        return "отличный"
    if score >= 75:
        return "хороший"
    if score >= 60:
        return "удовлетворительный"
    return "недостаточный"


# ============================================================
# Функции для анализа
# ============================================================

def student_summary(name: str, results: list[int]) -> dict:
    """Формирует итоговую статистику по одному студенту.

    Контракт:
    - Вход: имя студента и список его результатов.
    - Выход: словарь с ключами name, count, mean, min, max, category.
    - Особый случай: пустой список → mean/min/max = None, category = "нет данных".
    """
    if not results:
        return {
            "name": name,
            "count": 0,
            "mean": None,
            "min": None,
            "max": None,
            "category": "нет данных",
        }
    m = mean(results)
    return {
        "name": name,
        "count": len(results),
        "mean": m,
        "min": minimum(results),
        "max": maximum(results),
        "category": classify(m),
    }


def group_summary(students: dict[str, list[int]]) -> dict:
    """Общая статистика по группе.

    Контракт:
    - Вход: словарь {имя: список результатов}.
    - Выход: словарь с ключами total_students, total_scores, group_mean,
             category_counts, students_with_empty.
    - Особый случай: пустая группа → все нули/None.
    """
    if not students:
        return {
            "total_students": 0,
            "total_scores": 0,
            "group_mean": None,
            "category_counts": {
                "отличный": 0, "хороший": 0,
                "удовлетворительный": 0, "недостаточный": 0, "нет данных": 0,
            },
            "students_with_empty": [],
        }

    all_scores = []
    category_counts = {
        "отличный": 0, "хороший": 0,
        "удовлетворительный": 0, "недостаточный": 0, "нет данных": 0,
    }
    students_with_empty = []

    for name, results in students.items():
        if not results:
            students_with_empty.append(name)
            category_counts["нет данных"] += 1
            continue
        all_scores.extend(results)
        summary = student_summary(name, results)
        category_counts[summary["category"]] += 1

    group_mean = mean(all_scores) if all_scores else None

    return {
        "total_students": len(students),
        "total_scores": len(all_scores),
        "group_mean": group_mean,
        "category_counts": category_counts,
        "students_with_empty": students_with_empty,
    }


def find_top_students(students: dict[str, list[int]]) -> list[str]:
    """Находит студента(ов) с наибольшим средним баллом.

    Контракт:
    - Вход: словарь {имя: список результатов}.
    - Выход: список имён лидеров (может быть несколько при равенстве).
    - Особый случай: пустая группа или все с пустыми списками → [].
    - Исходный словарь не изменяется.
    """
    if not students:
        return []

    best_mean = None
    leaders = []

    for name, results in students.items():
        if not results:
            continue
        m = mean(results)
        if best_mean is None or m > best_mean:
            best_mean = m
            leaders = [name]
        elif m == best_mean:
            leaders.append(name)

    return leaders


def format_report(student_data: list[dict], group_data: dict, leaders: list[str]) -> str:
    """Формирует итоговый текстовый отчёт.

    Контракт:
    - Вход: список словарей по студентам, данные по группе, список лидеров.
    - Выход: многострочная строка с отчётом.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("ОТЧЁТ ПО УЧЕБНЫМ РЕЗУЛЬТАТАМ ГРУППЫ")
    lines.append("=" * 60)

    lines.append("\nРЕЗУЛЬТАТЫ СТУДЕНТОВ:")
    lines.append("-" * 60)
    for s in student_data:
        if s["mean"] is None:
            lines.append(f"  {s['name']}: нет результатов")
        else:
            lines.append(
                f"  {s['name']}: средний={s['mean']:.2f}, "
                f"мин={s['min']}, макс={s['max']}, "
                f"категория={s['category']}"
            )

    lines.append("\nСТАТИСТИКА ГРУППЫ:")
    lines.append("-" * 60)
    lines.append(f"  Всего студентов: {group_data['total_students']}")
    lines.append(f"  Всего оценок: {group_data['total_scores']}")
    if group_data['group_mean'] is not None:
        lines.append(f"  Средний балл группы: {group_data['group_mean']:.2f}")
    else:
        lines.append("  Средний балл группы: нет данных")

    lines.append("\n  Распределение по категориям:")
    for cat, count in group_data['category_counts'].items():
        if count > 0:
            lines.append(f"    {cat}: {count}")

    if group_data['students_with_empty']:
        lines.append(f"\n  Студенты без результатов: {', '.join(group_data['students_with_empty'])}")

    lines.append("\nЛИДЕРЫ:")
    lines.append("-" * 60)
    if leaders:
        lines.append(f"  {', '.join(leaders)}")
    else:
        lines.append("  Лидеров нет (группа пуста или нет результатов)")

    lines.append("=" * 60)
    return "\n".join(lines)


# ============================================================
# Основная логика
# ============================================================

def analyze(students: dict[str, list[int]]) -> str:
    """Главная функция: собирает всё вместе и возвращает отчёт."""
    # Статистика по каждому студенту
    student_data = []
    for name, results in students.items():
        student_data.append(student_summary(name, results))

    # Общая статистика
    group_data = group_summary(students)

    # Лидеры
    leaders = find_top_students(students)

    # Формируем отчёт
    return format_report(student_data, group_data, leaders)


# ============================================================
# Демонстрация
# ============================================================

if __name__ == "__main__":
    print(analyze(students))