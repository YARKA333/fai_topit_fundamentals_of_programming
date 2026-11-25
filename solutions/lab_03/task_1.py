LEVELS = ("недостаточный", "удовлетворительный", "хороший", "отличный")
ERROR_LABEL = "ошибка ввода"


def check_ranges(score: int, absences: int) -> str | None:
  if score < 0 or score > 100:
    return f"Некорректный результат: {score} (допустимо 0–100)"
  elif absences < 0 or absences > 5:
    return f"Некорректное число пропусков: {absences} (допустимо 0–5)"
  else:
    return None


def level_index(score: int) -> int:
  if score >= 90:
    return 3
  elif score >= 75:
    return 2
  elif score >= 60:
    return 1
  else:
    return 0


def level_name(score: int, absences: int) -> str:
  index = level_index(score)
  if absences > 3 and index > 0:
    index -= 1
  return LEVELS[index]


def describe_work(work_type: str) -> str:
  match work_type:
    case "exam":
      return "экзаменационная работа"
    case "project":
      return "проектная работа"
    case "practice":
      return "практическая работа"
    case _:
      return "неизвестный тип работы"


def evaluate(score: int, work_type: str, absences: int) -> tuple[str | None, str]:
  error = check_ranges(score, absences)
  if error is not None:
    return None, error  # ранний выход: классификация не выполняется
  level = level_name(score, absences)
  line = (
    f"{score:>3} | {describe_work(work_type)} | пропусков: {absences} "
    f"| уровень: {level}"
  )
  return level, line


# (score, work_type, absences, ожидаемый уровень или None для ошибки)
TEST_CASES: tuple[tuple[int, str, int, str | None], ...] = (
  (0, "exam", 0, "недостаточный"),
  (59, "project", 0, "недостаточный"),
  (60, "practice", 0, "удовлетворительный"),
  (74, "exam", 0, "удовлетворительный"),
  (75, "project", 0, "хороший"),
  (89, "practice", 0, "хороший"),
  (90, "exam", 0, "отличный"),
  (100, "project", 0, "отличный"),
  (90, "exam", 4, "хороший"),      # снижение на ступень
  (75, "exam", 3, "хороший"),      # 3 пропуска — не «более трёх»
  (60, "practice", 4, "недостаточный"),  # удовлетворительный -> недостаточный
  (20, "exam", 5, "недостаточный"),    # ниже нижнего уровня не опускается
  (101, "exam", 0, None),        # результат вне диапазона
  (50, "project", 6, None),        # пропуски вне диапазона
  (80, "lab", 1, "хороший"),       # неизвестный тип работы
)


def run_checks() -> list[tuple[int, str, int, str, str]]:
  rows = []
  for score, work_type, absences, expected in TEST_CASES:
    actual, _ = evaluate(score, work_type, absences)
    assert actual == expected, (score, work_type, absences, expected, actual)
    rows.append(
      (score, work_type, absences, expected or ERROR_LABEL, actual or ERROR_LABEL)
    )
  return rows


# --- Практическое расширение ------------------------------------------------
RECORDS: tuple[tuple[int, str, int], ...] = (
  (95, "exam", 0),
  (88, "project", 1),
  (72, "practice", 4),
  (59, "exam", 0),
  (60, "project", 2),
  (100, "practice", 5),
  (45, "exam", 3),
  (91, "project", 4),
  (75, "practice", 0),
  (120, "exam", 1),
  (66, "lab", 2),
  (84, "exam", 5),
)


def process_records(
  records: tuple[tuple[int, str, int], ...],
) -> tuple[list[str], dict[str, int]]:

  lines: list[str] = []
  counts = {level: 0 for level in LEVELS}
  counts[ERROR_LABEL] = 0
  for score, work_type, absences in records:
    level, line = evaluate(score, work_type, absences)
    lines.append(line)
    counts[level if level is not None else ERROR_LABEL] += 1
  return lines, counts



if __name__ == "__main__":
  print("== Одна запись ==")
  print(evaluate(82,"project",4)[1])

  print("\n== Тестовые сценарии ==")
  for score,work_type,absences,expected,actual in run_checks():
    print(f"{score:>3} {work_type:<8} {absences} | ожидалось: {expected:<20} | получено: {actual}")
  print("Все проверки пройдены.")

  print("\n== Список записей ==")
  snapshot=tuple(RECORDS)
  lines,counts=process_records(RECORDS)
  for line in lines:
    print(line)
  assert RECORDS==snapshot  # исходные данные не изменены
  print("\n== Сводка ==")
  for name,number in counts.items():
    print(f"{name}: {number}")
  assert sum(counts.values())==len(RECORDS)

  print("\n== Свой ввод ==")
  score=int(input("Результат (0–100): "))
  work_type=input("Тип работы (exam/project/practice): ").strip()
  absences=int(input("Пропусков (0–5): "))
  print(evaluate(score,work_type,absences)[1])
