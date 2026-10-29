import copy

# Исходная структура
original = [
    ["Python", 5],
    ["Algorithms", 4],
]

# Создаём три варианта "копий" разными способами
alias = original                    # просто ещё одно имя
shallow = original.copy()           # поверхностная копия
deep = copy.deepcopy(original)      # глубокая копия

# ============================================================
# Изменение 1: добавляем новый элемент во внешний список
# ============================================================
print("=== Изменение 1: original.append(['Databases', 5]) ===\n")
original.append(["Databases", 5])

for name, obj in [("original", original), ("alias", alias),
                  ("shallow", shallow), ("deep", deep)]:
    print(f"  {name:10s} = {obj}")
    print(f"    id = {id(obj)}")

print(f"\n  id первого вложенного списка:")
print(f"    original[0]: {id(original[0])}")
print(f"    alias[0]:    {id(alias[0])}")
print(f"    shallow[0]:  {id(shallow[0])}")
print(f"    deep[0]:     {id(deep[0])}")

print(f"\n  id объекта с первой оценкой (original[0][1]):")
print(f"    original[0][1]: {id(original[0][1])}")
print(f"    alias[0][1]:    {id(alias[0][1])}")
print(f"    shallow[0][1]:  {id(shallow[0][1])}")
print(f"    deep[0][1]:     {id(deep[0][1])}")

# ============================================================
# Изменение 2: меняем вложенный объект
# ============================================================
print("\n=== Изменение 2: original[0][1] = 3 ===\n")
original[0][1] = 3

for name, obj in [("original", original), ("alias", alias),
                  ("shallow", shallow), ("deep", deep)]:
    print(f"  {name:10s} = {obj}")

# ============================================================
# Ошибочная матрица
# ============================================================
print("\n=== Ошибочная матрица ===\n")
wrong_matrix = [[0] * 3] * 3
print("До изменения:")
for row in wrong_matrix:
    print(f"  {row}  (id={id(row)})")

wrong_matrix[0][0] = 1
print("\nПосле wrong_matrix[0][0] = 1:")
for row in wrong_matrix:
    print(f"  {row}")
#  Изменились все строки, потому что это один и тот же объект!

# ============================================================
# Правильная матрица
# ============================================================
print("\n=== Правильная матрица ===\n")
correct_matrix = [[0] * 3 for _ in range(3)]
print("До изменения:")
for row in correct_matrix:
    print(f"  {row}  (id={id(row)})")

correct_matrix[0][0] = 1
print("\nПосле correct_matrix[0][0] = 1:")
for row in correct_matrix:
    print(f"  {row}")
# Изменилась только первая строка, потому что строки — разные объекты.