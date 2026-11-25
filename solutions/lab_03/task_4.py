import math
from typing import Callable, Sequence


# --- Обязательные функции ---------------------------------------------------
def arithmetic_mean(values: list[float]) -> float:
  """Возвращает среднее арифметическое непустого списка.

  Для пустого списка контракт невыполним: возвращается nan (ранний выход).
  Переданный список не изменяется.
  """
  if not values:
    return math.nan
  total = 0.0
  for value in values:
    total += value
  return total / len(values)


def normalize_name(name: str) -> str:
  """Удаляет лишние пробелы и приводит каждую часть имени к виду «Иван».

  Части, разделённые дефисом, обрабатываются отдельно: «анна-мария» -> «Анна-Мария».
  """
  words = name.split()  # split() без аргумента убирает любые пробелы по краям и внутри
  if not words:
    return ""
  normalized = []
  for word in words:
    pieces = [piece.capitalize() for piece in word.split("-")]
    normalized.append("-".join(pieces))
  return " ".join(normalized)


def build_report(
  student: str,
  results: list[int],
  *,
  precision: int = 2,
  prefix: str = "Результат",
) -> str:
  """Формирует строковый отчёт о результатах студента.

  precision и prefix — только именованные параметры.
  """
  name = normalize_name(student)
  if not results:
    return f"{prefix}: {name} — результатов нет"
  mean = arithmetic_mean([float(r) for r in results])
  return f"{prefix}: {name} — среднее {mean:.{precision}f} (работ: {len(results)})"


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
  """Возвращает очищенные теги без пустых значений и повторов (порядок сохранён)."""
  seen: set[str] = set()
  cleaned: list[str] = []
  for tag in tags:
    value = tag.strip()
    if lowercase:
      value = value.lower()
    if not value or value in seen:
      continue
    seen.add(value)
    cleaned.append(value)
  return tuple(cleaned)


# --- Проверки (assert) ------------------------------------------------------
def run_asserts() -> None:
  # arithmetic_mean
  assert arithmetic_mean([1, 2, 3]) == 2.0
  assert arithmetic_mean([5]) == 5.0
  assert math.isnan(arithmetic_mean([]))
  data = [4.0, 6.0]
  arithmetic_mean(data)
  assert data == [4.0, 6.0]  # вход не изменён

  # normalize_name
  assert normalize_name("  иВАН   пЕТРОВ ") == "Иван Петров"
  assert normalize_name("анна-мария СИДОРОВА") == "Анна-Мария Сидорова"
  assert normalize_name("   ") == ""

  # build_report
  assert build_report("анна", [4, 5]) == "Результат: Анна — среднее 4.50 (работ: 2)"
  assert build_report("борис", [3, 4, 4], precision=1, prefix="Итог") == \
    "Итог: Борис — среднее 3.7 (работ: 3)"
  assert build_report("илья", []) == "Результат: Илья — результатов нет"
  marks = [5, 5]
  build_report("дарья", marks)
  assert marks == [5, 5]

  # collect_tags
  assert collect_tags("Python", " python ", "", "Loops") == ("python", "loops")
  assert collect_tags("A", "a", lowercase=False) == ("A", "a")
  assert collect_tags() == ()
  assert collect_tags("  ", "") == ()


# --- Исследование LEGB ------------------------------------------------------
course = "Программирование на Python"  # G — глобальная область


def outer() -> tuple[int, str]:
  counter = 0       # E — область объемлющей функции
  lesson = "лекция"   # E

  def inner() -> str:
    nonlocal counter  # привязываем имя к области outer, а не создаём локальное
    counter += 1    # изменяем E
    note = f"{course}: {lesson} №{counter}"  # L (note), G (course), E (lesson, counter)
    size = len(note)  # B — встроенная функция len
    return f"{note} (длина {size})"

  first = inner()
  inner()
  return counter, first


# --- Изменяемое значение по умолчанию ---------------------------------------
def add_result_buggy(value, results=[]):  # noqa: B006  (намеренная демонстрация)
  results.append(value)
  return results


def add_result(value, results=None):
  """Исправленная версия: новый список создаётся при каждом вызове."""
  if results is None:
    results = []
  results.append(value)
  return results


# --- Практическое расширение ------------------------------------------------
def apply_to_results(operation: Callable[[int], float], values: Sequence[int]) -> list[float]:
  """Применяет operation к каждому элементу; возвращает новый список."""
  return [operation(v) for v in values]


def percent(score: int) -> float:
  return score / 100


def make_threshold_checker(threshold: int) -> Callable[[int], bool]:
  """Фабрика: возвращает функцию, помнящую threshold в замыкании."""
  def check(score: int) -> bool:
    return score >= threshold
  return check


def main() -> None:
  run_asserts()
  print("Все assert-проверки пройдены.\n")

  print("== Позиционные и именованные аргументы ==")
  print(build_report("анна", [5, 4, 5]))
  print(build_report("борис", [3, 4], precision=0, prefix="Итог"))
  print(collect_tags("Python", "python ", "Циклы", lowercase=False))

  print("\n== Распаковка * и ** ==")
  args = ["дарья", [5, 5, 4]]
  kwargs = {"precision": 1, "prefix": "Оценка"}
  print(build_report(*args, **kwargs))
  tag_list = ["Списки", "словари", "СЛОВАРИ"]
  print(collect_tags(*tag_list))

  print("\n== LEGB ==")
  print("До вызова outer(): course =", repr(course))
  final_counter, first_note = outer()
  print("Первая заметка:", first_note)
  print("Итоговое значение counter в outer:", final_counter)
  print("После вызова outer(): course =", repr(course), "(не изменён)")
  assert final_counter == 2 and course == "Программирование на Python"

  print("\n== Изменяемое значение по умолчанию ==")
  print("buggy:", add_result_buggy(1), add_result_buggy(2))
  print("__defaults__ после двух вызовов:", add_result_buggy.__defaults__)
  print("fixed:", add_result(1), add_result(2))
  assert add_result_buggy.__defaults__ == ([1, 2],)
  assert add_result(1) == [1] and add_result(2) == [2]

  print("\n== Функции как аргументы и замыкания ==")
  scores = [55, 78, 91]
  print("named:", apply_to_results(percent, scores))
  print("lambda:", apply_to_results(lambda s: s + 5, scores))
  pass_60 = make_threshold_checker(60)
  pass_90 = make_threshold_checker(90)
  print("порог 60:", [pass_60(s) for s in scores])
  print("порог 90:", [pass_90(s) for s in scores])
  print("в замыкании:", pass_60.__closure__[0].cell_contents,
      pass_90.__closure__[0].cell_contents)
  assert [pass_60(s) for s in scores] == [False, True, True]
  assert [pass_90(s) for s in scores] == [False, False, True]
  assert scores == [55, 78, 91]


if __name__ == "__main__":
  main()
