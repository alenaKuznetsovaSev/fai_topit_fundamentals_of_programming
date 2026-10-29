# ============================================================
# Эксперимент A. Неизменяемый объект
# ============================================================
print("=== Эксперимент A ===")

# Прогноз: после a += 1 имя a будет ссылаться на НОВЫЙ объект 11,
# а b продолжит ссылаться на старый объект 10. id(a) изменится, id(b) — нет.
a = 10
b = a
print("До a += 1:")
print(f"  a = {a}, b = {b}")
print(f"  id(a) = {id(a)}, id(b) = {id(b)}")
print(f"  a is b: {a is b}")

a += 1
print("\nПосле a += 1:")
print(f"  a = {a}, b = {b}")
print(f"  id(a) = {id(a)}, id(b) = {id(b)}")
print(f"  a is b: {a is b}")

# ============================================================
# Эксперимент B. Изменяемый объект
# ============================================================
print("\n=== Эксперимент B ===")

# Прогноз: после second.append(30) оба имени будут показывать [10, 20, 30],
# потому что first и second ссылаются на один и тот же список.
first = [10, 20]
second = first
print("До append:")
print(f"  first = {first}, second = {second}")
print(f"  id(first) = {id(first)}, id(second) = {id(second)}")
print(f"  first is second: {first is second}")

second.append(30)
print("\nПосле second.append(30):")
print(f"  first = {first}, second = {second}")
print(f"  id(first) = {id(first)}, id(second) = {id(second)}")

# Дополнительные действия: переназначаем second на новый список
print("\n--- Переназначение second ---")
second = [10, 20, 30]
print(f"  first = {first}, second = {second}")
print(f"  id(first) = {id(first)}, id(second) = {id(second)}")
print(f"  first == second: {first == second}")
print(f"  first is second: {first is second}")

# Изменяем новый second и проверяем, повлияло ли это на first
second.append(40)
print("\nПосле second.append(40):")
print(f"  first = {first}")
print(f"  second = {second}")
print("first не изменился, потому что second теперь ссылается на другой объект.")

# ============================================================
# Практическая задача: конфигурации проекта
# ============================================================
print("\n=== Практическая задача ===")

# Первая конфигурация — исходная
config_a = {
    "name": "Проект Альфа",
    "participants": ["Анна", "Борис"],
    "run_params": ["--verbose", "--threads=4"]
}

# Пытаемся сделать "копию" простым присваиванием
config_b = config_a

print("До изменений:")
print(f"  config_a = {config_a}")
print(f"  config_b = {config_b}")
print(f"  config_a is config_b: {config_a is config_b}")

# Меняем config_b — но изменения затрагивают и config_a!
config_b["participants"].append("Виктор")
config_b["run_params"].append("--debug")

print("\nПосле изменений в config_b:")
print(f"  config_a = {config_a}")
print(f"  config_b = {config_b}")
print("⚠️ config_a тоже изменился! Это нежелательное совместное изменение.")

# Теперь создаём действительно независимую копию через глубокое копирование
import copy
config_c = copy.deepcopy(config_a)

print("\n--- После deepcopy в config_c ---")
config_c["participants"].append("Галина")
config_c["run_params"].append("--log=all")

print(f"  config_a = {config_a}")
print(f"  config_c = {config_c}")

# Проверяем независимость через assert
assert config_a["participants"] != config_c["participants"], "Списки участников не должны совпадать"
assert config_a["run_params"] != config_c["run_params"], "Параметры запуска не должны совпадать"
assert config_a is not config_c, "Это должны быть разные объекты"
print("\n✅ Все assert прошли — config_c полностью независима от config_a.")