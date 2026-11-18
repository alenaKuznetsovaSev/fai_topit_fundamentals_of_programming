"""
Работа с коллекциями: множества, словари, выбор структуры данных.
Построение индексов по данным о сдаче лабораторных работ.
"""

# ============================================================
# Исходные данные
# ============================================================
submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),  # повторная попытка
]

print("Исходные данные:")
for s in submissions:
    print(f"  {s}")
print()

# ============================================================
# 1. Множество всех студентов
# ============================================================
students = set()
for student, _, _ in submissions:
    students.add(student)
print(f"Все студенты: {sorted(students)}")

# ============================================================
# 2. Множество всех сданных лабораторных работ
# ============================================================
labs = set()
for _, lab, _ in submissions:
    labs.add(lab)
print(f"Все лабораторные: {sorted(labs)}")

# ============================================================
# 3. Словарь: студент → список его попыток
# ============================================================
attempts_by_student = {}
for student, lab, grade in submissions:
    if student not in attempts_by_student:
        attempts_by_student[student] = []
    attempts_by_student[student].append((lab, grade))

print("\nПопытки по студентам:")
for student, attempts in sorted(attempts_by_student.items()):
    print(f"  {student}: {attempts}")

# ============================================================
# 4. Словарь лучших результатов по ключу (student, lab)
# ============================================================
best_results = {}
for student, lab, grade in submissions:
    key = (student, lab)
    if key not in best_results or grade > best_results[key]:
        best_results[key] = grade

print("\nЛучшие результаты (student, lab) → grade:")
for key, grade in sorted(best_results.items()):
    print(f"  {key}: {grade}")

# ============================================================
# 5. Словарь количества попыток для каждой пары (student, lab)
# ============================================================
attempts_count = {}
for student, lab, _ in submissions:
    key = (student, lab)
    attempts_count[key] = attempts_count.get(key, 0) + 1

print("\nКоличество попыток:")
for key, count in sorted(attempts_count.items()):
    print(f"  {key}: {count}")

# ============================================================
# 6. Студенты, сдававшие обе работы (через операции над множествами)
# ============================================================
# Собираем множества работ для каждого студента
labs_per_student = {}
for student, lab, _ in submissions:
    if student not in labs_per_student:
        labs_per_student[student] = set()
    labs_per_student[student].add(lab)

# Находим студентов, у которых есть и lab_01, и lab_02
required_labs = {"lab_01", "lab_02"}
students_with_both = set()
for student, their_labs in labs_per_student.items():
    if required_labs.issubset(their_labs):
        students_with_both.add(student)

print(f"\nСтуденты, сдавшие обе работы: {sorted(students_with_both)}")

# Альтернатива через пересечение:
# students_with_both_alt = {s for s, labs in labs_per_student.items()
#                            if labs & required_labs == required_labs}

# ============================================================
# 7. Добавление новой записи без полного перестроения
# ============================================================
print("\n--- Добавляем новую запись: ('ekaterina', 'lab_01', 5) ---")
new_record = ("ekaterina", "lab_01", 5)
student, lab, grade = new_record

# Обновляем все структуры инкрементально
students.add(student)
labs.add(lab)

if student not in attempts_by_student:
    attempts_by_student[student] = []
attempts_by_student[student].append((lab, grade))

key = (student, lab)
if key not in best_results or grade > best_results[key]:
    best_results[key] = grade

attempts_count[key] = attempts_count.get(key, 0) + 1

if student not in labs_per_student:
    labs_per_student[student] = set()
labs_per_student[student].add(lab)

# Проверяем, не попала ли ekaterina в "сдал обе работы" (не должна — только lab_01)
students_with_both_updated = {
    s for s, their_labs in labs_per_student.items()
    if required_labs.issubset(their_labs)
}
print(f"Студенты с обеими работами после добавления: {sorted(students_with_both_updated)}")
print("(ekaterina не попала — у неё только lab_01)")

# ============================================================
# Практическое расширение: текстовые запросы
# ============================================================
print("\n" + "=" * 50)
print("ТЕКСТОВЫЕ ЗАПРОСЫ")
print("=" * 50)

queries = [
    "student anna",
    "best anna lab_01",
    "attempts boris lab_02",
    "completed lab_01",
    "student unknown_student",
    "best anna lab_99",
    "unknown_command",
]


def handle_query(query: str) -> None:
    """Обрабатывает текстовый запрос и выводит результат."""
    parts = query.strip().split()
    if not parts:
        print(f"  Запрос: '{query}' → пустой запрос")
        return

    command = parts[0]

    match command:
        case "student":
            if len(parts) != 2:
                print(f"  Запрос: '{query}' → ожидается: student <name>")
                return
            name = parts[1]
            if name in attempts_by_student:
                print(f"  Запрос: '{query}'")
                print(f"    → Попытки {name}: {attempts_by_student[name]}")
            else:
                print(f"  Запрос: '{query}' → студент '{name}' не найден")

        case "best":
            if len(parts) != 3:
                print(f"  Запрос: '{query}' → ожидается: best <student> <lab>")
                return
            name, lab = parts[1], parts[2]
            key = (name, lab)
            if key in best_results:
                print(f"  Запрос: '{query}' → лучший результат: {best_results[key]}")
            else:
                print(f"  Запрос: '{query}' → пара ({name}, {lab}) не найдена")

        case "attempts":
            if len(parts) != 3:
                print(f"  Запрос: '{query}' → ожидается: attempts <student> <lab>")
                return
            name, lab = parts[1], parts[2]
            key = (name, lab)
            count = attempts_count.get(key, 0)
            print(f"  Запрос: '{query}' → количество попыток: {count}")

        case "completed":
            if len(parts) != 2:
                print(f"  Запрос: '{query}' → ожидается: completed <lab>")
                return
            lab = parts[1]
            # Находим студентов, у которых есть эта работа в лучших результатах
            completers = sorted({
                student for (student, l), _ in best_results.items()
                if l == lab
            })
            print(f"  Запрос: '{query}' → сдали: {completers}")

        case _:
            print(f"  Запрос: '{query}' → неизвестная команда '{command}'")


for q in queries:
    handle_query(q)
    print()