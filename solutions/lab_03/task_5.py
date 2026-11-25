"""
Правила, выбранные заранее:
  * студент с пустым списком результатов получает категорию «нет данных»,
  его среднее/минимум/максимум равны None;
  * такие студенты не участвуют в общей статистике, рейтинге и выборе лидеров,
  но учитываются в счётчике «нет данных»;
  * рейтинг: по среднему по убыванию, при равенстве — по имени по возрастанию;
  * «общий средний» — среднее по всем отдельным результатам группы.
"""

students = {
  "Анна": [78, 91, 84, 88],
  "Борис": [60, 72, 68],
  "Дарья": [95, 93, 97, 90],
  "Илья": [55, 61],
}

CATEGORIES = ("отличный", "хороший", "удовлетворительный", "недостаточный")
NO_DATA = "нет данных"


def mean(values: list[float]) -> float | None:
  """Среднее арифметическое; для пустого списка — None. O(n)."""
  if not values:
    return None
  total = 0
  for value in values:
    total += value
  return total / len(values)


def minimum(values: list[float]) -> float | None:
  """Минимум без min(); для пустого списка — None. O(n)."""
  if not values:
    return None
  result = values[0]
  for value in values:
    if value < result:
      result = value
  return result


def maximum(values: list[float]) -> float | None:
  """Максимум без max(); для пустого списка — None. O(n)."""
  if not values:
    return None
  result = values[0]
  for value in values:
    if value > result:
      result = value
  return result


def classify(score: float | None) -> str:
  """Категория по числу 0–100 (None -> «нет данных»)."""
  if score is None:
    return NO_DATA
  if score >= 90:
    return "отличный"
  elif score >= 75:
    return "хороший"
  elif score >= 60:
    return "удовлетворительный"
  else:
    return "недостаточный"


def student_summary(name: str, results: list[float]) -> dict:
  """Итоги одного студента. Список results не изменяется."""
  average = mean(results)
  return {
    "name": name,
    "count": len(results),
    "mean": average,
    "min": minimum(results),
    "max": maximum(results),
    "category": classify(average),
  }


def group_summary(students: dict[str, list[float]]) -> dict:
  """Статистика группы за один проход по студентам и их результатам.

  O(N), где N — общее число результатов; память O(S) под сводки студентов.
  """
  summaries: list[dict] = []
  category_counts = {category: 0 for category in CATEGORIES}
  category_counts[NO_DATA] = 0
  all_total = 0
  all_count = 0
  for name, results in students.items():
    summary = student_summary(name, results)
    summaries.append(summary)
    category_counts[summary["category"]] += 1
    for value in results:
      all_total += value
      all_count += 1
  return {
    "students": len(students),
    "with_results": len(summaries) - category_counts[NO_DATA],
    "overall_mean": (all_total / all_count) if all_count else None,
    "category_counts": category_counts,
    "summaries": summaries,
  }


def ranking(summaries: list[dict]) -> list[dict]:
  """Рейтинг на копии: вставками, по среднему (убыв.), затем по имени."""
  rated: list[dict] = []
  for item in summaries:
    if item["mean"] is None:
      continue
    position = len(rated)
    while position > 0:
      prev = rated[position - 1]
      if (item["mean"], prev["name"]) > (prev["mean"], item["name"]):
        position -= 1
      else:
        break
    rated.insert(position, item)
  return rated


def find_top_students(students: dict[str, list[float]]) -> list[str]:
  """Имена студентов с наибольшим средним; пустая группа -> []."""
  best: float | None = None
  leaders: list[str] = []
  for name, results in students.items():
    average = mean(results)
    if average is None:
      continue
    if best is None or average > best:
      best = average
      leaders = [name]
    elif average == best:
      leaders.append(name)
  return leaders


def _fmt(value: float | None) -> str:
  return "—" if value is None else f"{value:.2f}"


def format_report(student_data: list[dict], group_data: dict) -> str:
  """Итоговый текстовый отчёт: по студентам, рейтинг, сводка группы."""
  lines = ["Результаты по студентам:"]
  for s in student_data:
    lines.append(
      f"  {s['name']}: среднее {_fmt(s['mean'])}, мин {_fmt(s['min'])}, "
      f"макс {_fmt(s['max'])}, категория: {s['category']}"
    )
  lines.append("Рейтинг:")
  rated = ranking(student_data)
  if not rated:
    lines.append("  нет данных")
  for place, s in enumerate(rated, start=1):
    lines.append(f"  {place}. {s['name']} — {_fmt(s['mean'])}")
  lines.append("Группа:")
  lines.append(f"  студентов: {group_data['students']} "
         f"(с результатами: {group_data['with_results']})")
  lines.append(f"  общий средний результат: {_fmt(group_data['overall_mean'])}")
  for category, number in group_data["category_counts"].items():
    lines.append(f"  {category}: {number}")
  return "\n".join(lines)


def analyze(group: dict[str, list[float]]) -> tuple[str, list[str]]:
  """Полный цикл: отчёт и список лидеров."""
  data = group_summary(group)
  report = format_report(data["summaries"], data)
  return report, find_top_students(group)


# --- Сценарии проверки ------------------------------------------------------
def scenarios() -> list[tuple[str, dict, list[str], str | None, dict]]:
  """(название, данные, ожидаемые лидеры, ожидаемый общий средний, счётчики)."""
  return [
    ("обычный набор данных", students, ["Дарья"], "79.38",
     {"отличный": 1, "хороший": 1, "удовлетворительный": 1, "недостаточный": 1}),
    ("один студент", {"Олег": [80, 90]}, ["Олег"], "85.00",
     {"хороший": 1}),
    ("несколько лидеров", {"А": [90, 80], "Б": [85, 85], "В": [70]},
     ["А", "Б"], "82.00", {"хороший": 2, "удовлетворительный": 1}),
    ("пустая группа", {}, [], None, {}),
    ("студент без результатов", {"Мария": [], "Петр": [70]}, ["Петр"],
     "70.00", {"нет данных": 1, "удовлетворительный": 1}),
    ("граничные значения категорий",
     {"a": [90], "b": [89], "c": [75], "d": [74], "e": [60], "f": [59]},
     ["a"], "74.50",
     {"отличный": 1, "хороший": 2, "удовлетворительный": 2, "недостаточный": 1}),
  ]


def run_checks() -> list[tuple[str, str, str, str]]:
  """Выполняет сценарии. Возвращает строки: название, лидеры, общий средний, статус."""
  rows = []
  for title, data, leaders, overall, counts in scenarios():
    snapshot = {k: list(v) for k, v in data.items()}
    summary = group_summary(data)
    assert find_top_students(data) == leaders, title
    assert _fmt(summary["overall_mean"]) == (overall or "—"), title
    for category, number in counts.items():
      assert summary["category_counts"][category] == number, (title, category)
    assert data == snapshot, title  # исходный словарь не изменён
    rows.append((title, ", ".join(leaders) or "—", overall or "—", "пройден"))
  # отдельные проверки функций
  assert mean([]) is None and minimum([]) is None and maximum([]) is None
  assert (minimum([4, 2, 9]), maximum([4, 2, 9]), mean([4, 2, 9])) == (2, 9, 5.0)
  assert [classify(x) for x in (0, 59, 60, 74, 75, 89, 90, 100)] == [
    "недостаточный", "недостаточный", "удовлетворительный", "удовлетворительный",
    "хороший", "хороший", "отличный", "отличный"]
  return rows


def main() -> None:
  report, leaders = analyze(students)
  print(report)
  print("Лидеры:", ", ".join(leaders))

  print("\n== Сценарии проверки ==")
  for title, leaders_text, overall, status in run_checks():
    print(f"{title:<32} лидеры: {leaders_text:<10} общий средний: {overall:<6} {status}")
  print("Все проверки пройдены.")


if __name__ == "__main__":
  main()
