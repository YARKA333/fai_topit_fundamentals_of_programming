
submissions = [
  ("anna", "lab_01", 5),
  ("boris", "lab_01", 4),
  ("anna", "lab_02", 5),
  ("daria", "lab_01", 3),
  ("boris", "lab_02", 5),
  ("anna", "lab_01", 4),
]



def add_submission(db: dict, student: str, lab: str, score: int) -> None:
  """Добавляет запись, обновляя все структуры за O(1) в среднем."""
  key = (student, lab)  # кортеж хешируем -> подходит как ключ
  db["students"].add(student)
  db["labs"].add(lab)
  db["attempts"].setdefault(student, []).append((lab, score))
  if key not in db["best"] or score > db["best"][key]:
    db["best"][key] = score
  db["counts"][key] = db["counts"].get(key, 0) + 1
  db["by_lab"].setdefault(lab, set()).add(student)


def build_db(records: list[tuple[str, str, int]]) -> dict:
  """Построение структур по списку записей; исходный список не меняется.

  students  : set[str]             — уникальные студенты
  labs    : set[str]             — уникальные работы
  attempts  : dict[str, list[(lab, score)]]  — попытки студента
  best    : dict[(student, lab), int]    — лучший результат
  counts  : dict[(student, lab), int]    — число попыток
  by_lab  : dict[str, set[str]]      — кто сдавал работу
  """
  db={
    "students": set(),
    "labs": set(),
    "attempts": {},
    "best": {},
    "counts": {},
    "by_lab": {},
  }
  for student, lab, score in records:
    add_submission(db, student, lab, score)
  return db


def students_with_all_labs(db: dict) -> set[str]:
  """Студенты, сдававшие все работы: пересечение множеств по работам."""
  if not db["by_lab"]:
    return set()  # ранний выход: пересекать нечего
  return set.intersection(*db["by_lab"].values())


def handle_query(db: dict, line: str) -> str:
  parts = line.split()
  match parts:
    case []:
      return "Пустая команда"
    case ["student", name]:
      if name not in db["attempts"]:
        return f"Студент {name!r} не найден"
      items = [f"{lab}: {score}" for lab, score in db["attempts"][name]]
      return f"Попытки {name}: " + ", ".join(items)
    case ["best", name, lab]:
      key = (name, lab)
      if key not in db["best"]:
        return f"Нет данных для пары {name!r}, {lab!r}"
      return f"Лучший результат {name} по {lab}: {db['best'][key]}"
    case ["attempts", name, lab]:
      key = (name, lab)
      if key not in db["counts"]:
        return f"Нет данных для пары {name!r}, {lab!r}"
      return f"Попыток {name} по {lab}: {db['counts'][key]}"
    case ["completed", lab]:
      if lab not in db["by_lab"]:
        return f"Работа {lab!r} не найдена"
      return f"{lab} сдавали: " + ", ".join(sorted(db["by_lab"][lab]))
    case _:
      return f"Неизвестная команда или неверное число аргументов: {line!r}"


if __name__ == "__main__":
  snapshot=list(submissions)
  db=build_db(submissions)
  assert submissions==snapshot

  print("1. Студенты:",sorted(db["students"]))
  print("2. Работы:  ",sorted(db["labs"]))
  print("3. Попытки по студентам:")
  for student in sorted(db["attempts"]):
    print("  ",student,db["attempts"][student])
  print("4. Лучшие результаты:")
  for key in sorted(db["best"]):
    print("  ",key,db["best"][key])
  print("5. Число попыток:")
  for key in sorted(db["counts"]):
    print("  ",key,db["counts"][key])

  both=db["by_lab"]["lab_01"]&db["by_lab"]["lab_02"]
  print("\nСдавали обе работы:",sorted(both))
  assert both=={"anna","boris"}
  assert db["best"][("anna","lab_01")]==5
  assert db["counts"][("anna","lab_01")]==2
  assert db["counts"][("daria","lab_01")]==1
  assert students_with_all_labs(db)==both

  print("\n== Добавление записей без пересборки ==")
  add_submission(db,"daria","lab_02",4)
  add_submission(db,"boris","lab_01",5)
  print("Сдавали обе работы:",sorted(students_with_all_labs(db)))
  print("Лучший boris/lab_01:",db["best"][("boris","lab_01")],
        "| попыток:",db["counts"][("boris","lab_01")])
  assert students_with_all_labs(db)=={"anna","boris","daria"}
  assert db["best"][("boris","lab_01")]==5
  assert db["counts"][("boris","lab_01")]==2
  # результат совпадает с полной пересборкой
  rebuilt=build_db(submissions+[("daria","lab_02",4),("boris","lab_01",5)])
  assert rebuilt==db

  print("\n== Текстовые запросы ==")
  queries=[
    "student anna",
    "best anna lab_01",
    "attempts boris lab_02",
    "completed lab_01",
    "student zoya",
    "best anna lab_09",
    "completed lab_77",
    "best anna",
    "hello world",
    "",
  ]
  for q in queries:
    print(f"> {q}\n  {handle_query(db,q)}")
  assert handle_query(db,"best anna lab_01")=="Лучший результат anna по lab_01: 5"
  assert handle_query(db,"attempts boris lab_02")=="Попыток boris по lab_02: 1"
  assert "не найден" in handle_query(db,"student zoya")
  assert "Неизвестная" in handle_query(db,"hello world")
