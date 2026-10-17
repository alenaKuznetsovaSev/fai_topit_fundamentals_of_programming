"""
Программа собирает данные о вычислительном эксперименте
и выводит красивую карточку с результатами.
"""

# Спрашиваем у пользователя данные
researcher = input("Имя исследователя: ")
experiment_name = input("Название эксперимента: ")
runs = int(input("Количество запусков: "))
duration_sec = float(input("Длительность одного запуска (сек): "))
real_part = float(input("Действительная часть коэффициента: "))
imag_part = float(input("Мнимая часть коэффициента: "))

# Считаем нужные значения
total_sec = runs * duration_sec
total_min = total_sec / 60
coeff = complex(real_part, imag_part)
mod_sq = real_part ** 2 + imag_part ** 2
has_runs = bool(runs)

# Красивый вывод карточки
print()
print("=" * 40)
print(f"ЭКСПЕРИМЕНТ: {experiment_name}")
print(f"Исследователь: {researcher}")
print(f"Запуски: {runs}")
print(f"Общее время: {total_sec:.2f} с ({total_min:.2f} мин)")
print(f"Коэффициент: {coeff}")
print(f"Квадрат модуля: {mod_sq:.2f}")
print(f"Есть выполненные запуски: {has_runs}")
print("=" * 40)

# Смотрим, какие типы у нас получились на самом деле
print("\nТипы введенных данных:")
print(f"  researcher     -> {type(researcher)}")
print(f"  experiment     -> {type(experiment_name)}")
print(f"  runs           -> {type(runs)}")
print(f"  duration_sec   -> {type(duration_sec)}")
print(f"  real_part      -> {type(real_part)}")
print(f"  imag_part      -> {type(imag_part)}")