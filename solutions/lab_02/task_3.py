import sys
import weakref

# ============================================================
# Эксперимент 1. Подсчёт ссылок через sys.getrefcount()
# ============================================================
print("=== Эксперимент 1: подсчёт ссылок ===\n")

data = [1, 2, 3]
print(f"После создания:              {sys.getrefcount(data)}")
# Прогноз: 2 (одна от data, одна временная при передаче в getrefcount)

alias = data
print(f"После создания alias:        {sys.getrefcount(data)}")
# Прогноз: 3 (+1 от alias)

container = [data]
print(f"После помещения в контейнер: {sys.getrefcount(data)}")
# Прогноз: 4 (+1 от container[0])

del alias
print(f"После del alias:             {sys.getrefcount(data)}")
# Прогноз: 3

container.clear()
print(f"После очистки контейнера:    {sys.getrefcount(data)}")
# Прогноз: 2

# ============================================================
# Эксперимент 2. Слабая ссылка
# ============================================================
print("\n=== Эксперимент 2: слабая ссылка ===\n")

class Record:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Record({self.name!r})"

record = Record("alpha")
weak_record = weakref.ref(record)

print(f"Сильная ссылка жива:  record = {record}")
print(f"Слабая ссылка:        weak_record() = {weak_record()}")

del record
print("\nПосле del record:")
print(f"Слабая ссылка:        weak_record() = {weak_record()}")
print("Слабая ссылка вернула None — объект удалён сборщиком мусора.")

# ============================================================
# Практическая задача. Слабый реестр объектов
# ============================================================
print("\n=== Практическая задача: WeakValueDictionary ===\n")

registry = weakref.WeakValueDictionary()

# Создаём три объекта Record
obj_a = Record("alpha")
obj_b = Record("beta")
obj_c = Record("gamma")

# Регистрируем все три в слабом словаре
registry["a"] = obj_a
registry["b"] = obj_b
registry["c"] = obj_c

# Сильные ссылки оставляем только на obj_a и obj_b
# obj_c существует только благодаря записи в слабом словаре

print("Изначально в реестре:")
print(f"  keys = {list(registry.keys())}")
print(f"  values = {list(registry.values())}")

# Удаляем сильную ссылку на obj_c
del obj_c
print("\nПосле del obj_c (сильной ссылки больше нет):")
print(f"  keys = {list(registry.keys())}")
# Запись 'c' исчезла автоматически — объект был удалён.

# Удаляем сильную ссылку на obj_b
del obj_b
print("\nПосле del obj_b:")
print(f"  keys = {list(registry.keys())}")
# Остался только obj_a — единственная сильная ссылка.

# obj_a всё ещё жива — её можно достать из реестра
print(f"\nobj_a из реестра: {registry['a']}")