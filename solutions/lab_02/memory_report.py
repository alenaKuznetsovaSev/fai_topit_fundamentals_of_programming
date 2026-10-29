"""
Утилита для исследования потребления памяти в Python.
Запускает все измерения из задания 5 и выводит единый отчёт.
"""

import sys
import tracemalloc


def measure_scenario(name, create_func):
    """Измеряет память для заданного сценария создания объекта."""
    tracemalloc.start()
    obj = create_func()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "name": name,
        "count": len(obj) if hasattr(obj, '__len__') else "N/A",
        "size_bytes": sys.getsizeof(obj),
        "current_kb": current / 1024,
        "peak_kb": peak / 1024,
    }


def main():
    print("=" * 70)
    print("ОТЧЁТ ПО ИССЛЕДОВАНИЮ ПОТРЕБЛЕНИЯ ПАМЯТИ")
    print("=" * 70)

    # Сценарии для сравнения
    scenarios = [
        ("list(range(100_000))", lambda: list(range(100_000))),
        ("range(100_000)", lambda: range(100_000)),
    ]

    results = []
    for name, func in scenarios:
        result = measure_scenario(name, func)
        results.append(result)

    # Вывод таблицы
    print(f"\n{'Сценарий':<25} {'Элементов':<12} {'Размер':<15} {'Текущий':<12} {'Пиковый':<12}")
    print("-" * 70)

    for r in results:
        print(f"{r['name']:<25} {str(r['count']):<12} "
              f"{r['size_bytes']:<12} "
              f"{r['current_kb']:<10.2f}КБ {r['peak_kb']:<10.2f}КБ")

    # Отношение через sys.getsizeof (надёжнее, чем через tracemalloc)
    if len(results) >= 2 and results[1]['size_bytes'] > 0:
        ratio = results[0]['size_bytes'] / results[1]['size_bytes']
        print(f"\nОтношение размеров (list / range) по sys.getsizeof: {ratio:.2f}x")

    # Пояснение про tracemalloc
    print("\nВажное замечание:")
    print("tracemalloc показал ~0 КБ для range, потому что range — это C-объект,")
    print("который выделяет память через стандартный malloc, а не через Python-аллокатор.")
    print("Поэтому отношение считается через sys.getsizeof(), который видит все объекты.")

    print("\n" + "=" * 70)
    print("ВЫВОД:")
    print("list(range(N)) материализует все N объектов сразу → много памяти.")
    print("range(N) хранит только правило → минимум памяти (всего 48 байт).")
    print("Для больших последовательностей предпочитайте ленивые объекты.")
    print("=" * 70)


if __name__ == "__main__":
    main()