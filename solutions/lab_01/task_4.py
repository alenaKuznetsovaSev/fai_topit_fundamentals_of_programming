
student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10

# 1. Первый и последний символ имени
print("1. Первый символ:", student[0])
print("   Последний символ:", student[-1])

# 2. Срезы с именем и фамилией
print("2. Имя:", student[:4])
print("   Фамилия:", student[5:])

# 3. Верхний и нижний регистр
print("3. Верхний регистр:", student.upper())
print("   Нижний регистр:", student.lower())

# 4. Инициалы с помощью индексации
# "Анна Смирнова": индекс 0 - 'А', индекс 5 - 'С'
initials = student[0] + "." + student[5] + "."
print("4. Инициалы:", initials)

# 5. Курс в обратном порядке (срез с шагом -1)
print("5. Курс наоборот:", course[::-1])

# 6. Форматирование строки результата тремя способами
percent = completed / total * 100
print("6. Форматирование:")
# Способ 1: оператор %
print("   %s — %s: %d/%d (%.1f%%)" % (student, course, completed, total, percent))
# Способ 2: метод .format()
print("   {} — {}: {}/{} ({:.1f}%)".format(student, course, completed, total, percent))
# Способ 3: f-строка
print(f"   {student} — {course}: {completed}/{total} ({percent:.1f}%)")

# 7. Исследование Unicode
symbol = "Я"
print("7. Unicode:")
print("   Символ:", symbol)
print("   Код (ord):", ord(symbol))
print("   Восстановленный (chr):", chr(ord(symbol)))
encoded = symbol.encode("utf-8")
print("   UTF-8 байты:", encoded)
print("   Длина байтов:", len(encoded))

# 8. Попытка изменения строки (намеренная ошибка)
# student[0] = "О"
# TypeError: 'str' object does not support item assignment
