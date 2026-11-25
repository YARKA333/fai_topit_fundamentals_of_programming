
MEASUREMENTS = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]


def single_pass_stats(values: list[int]) -> dict[str, int] | None:
  if not values:
    return None  # ранний выход: статистики пустого списка не существует
  total = 0
  minimum = values[0]
  maximum = values[0]
  even_count = 0
  for value in values:
    total += value
    if value < minimum:
      minimum = value
    if value > maximum:
      maximum = value
    if value % 2 == 0:
      even_count += 1
  return {"sum": total, "min": minimum, "max": maximum, "even": even_count}


def count_above_mean(values: list[int], mean: float) -> int:
  count = 0
  for value in values:
    if value > mean:
      count += 1
  return count


def linear_search(values: list[int], target: int) -> tuple[int, int]:
  comparisons = 0
  for index, value in enumerate(values):
    comparisons += 1
    if value == target:
      return index, comparisons
  return -1, comparisons


def is_prime(n: int) -> tuple[bool, int]:
  """Простота n > 0 и число проверенных делителей. O(sqrt(n)), O(1).

  Условие d * d <= n эквивалентно d <= sqrt(n) и не использует float.
  """
  if n < 2:
    return False, 0
  checked = 0
  divisor = 2
  while divisor * divisor <= n:
    checked += 1
    if n % divisor == 0:
      return False, checked
    divisor += 1
  return True, checked


def selection_sort(values: list[int]) -> tuple[list[int], int]:
  result = list(values)
  comparisons = 0
  n = len(result)
  for i in range(n - 1):
    smallest = i
    for j in range(i + 1, n):
      comparisons += 1
      if result[j] < result[smallest]:
        smallest = j
    result[i], result[smallest] = result[smallest], result[i]
  return result, comparisons


def binary_search(sorted_values: list[int], target: int) -> tuple[int, int]:
  """Бинарный поиск. Возвращает (индекс или -1, сравнения). O(log n), O(1).

  Одна итерация = одно трёхстороннее сравнение элемента с искомым.
  """
  low, high = 0, len(sorted_values) - 1
  comparisons = 0
  while low <= high:
    mid = (low + high) // 2
    comparisons += 1
    if sorted_values[mid] == target:
      return mid, comparisons
    elif sorted_values[mid] < target:
      low = mid + 1
    else:
      high = mid - 1
  return -1, comparisons


# --- Эксперимент ------------------------------------------------------------
def make_dataset(n: int) -> list[int]:
  """Детерминированный «перемешанный» набор из n различных чисел."""
  modulus = 3 * n + 1
  data = [(i * 7919 + 13) % modulus for i in range(n)]
  assert len(set(data)) == n
  return data


def compare_searches(sizes: tuple[int, ...] = (10, 100, 1000)) -> list[tuple]:
  """Строки таблицы: n, линейный (средн., худш.), бинарный (средн., худш.)."""
  rows = []
  for n in sizes:
    data = make_dataset(n)
    sorted_data, sort_cmp = selection_sort(data)
    assert sort_cmp == n * (n - 1) // 2

    lin_total = 0
    bin_total = 0
    bin_worst = 0
    for target in data:
      index, c = linear_search(data, target)
      assert data[index] == target
      lin_total += c
      index, c = binary_search(sorted_data, target)
      assert sorted_data[index] == target
      bin_total += c
      if c > bin_worst:
        bin_worst = c

    missing = -1  # в наборе только неотрицательные числа
    lin_miss = linear_search(data, missing)[1]
    bin_miss = binary_search(sorted_data, missing)[1]
    if bin_miss > bin_worst:
      bin_worst = bin_miss
    rows.append((n, lin_total / n, lin_miss, bin_total / n, bin_worst, sort_cmp))
  return rows


if __name__ == "__main__":
  stats=single_pass_stats(MEASUREMENTS)
  assert stats is not None
  mean=stats["sum"]/len(MEASUREMENTS)
  above=count_above_mean(MEASUREMENTS,mean)
  print("Данные:",MEASUREMENTS)
  print(f"Сумма: {stats['sum']}, минимум: {stats['min']}, максимум: {stats['max']}")
  print(f"Чётных: {stats['even']}, среднее: {mean}, выше среднего: {above}")
  assert stats=={"sum":144,"min":7,"max":21,"even":4}
  assert mean==14.4 and above==6

  print("\n== Линейный поиск ==")
  for target in [18,7,100]:
    index,comparisons=linear_search(MEASUREMENTS,target)
    print(f"{target}: индекс {index}, сравнений {comparisons}")
  assert linear_search(MEASUREMENTS,18)==(3,4)
  assert linear_search(MEASUREMENTS,100)==(-1,10)

  print("\n== Проверка простоты ==")
  for n in (1,2,17,18,97,100,7919):
    prime,checked=is_prime(n)
    print(f"{n}: {'простое' if prime else 'не простое'}, делителей проверено: {checked}")
  assert [is_prime(n)[0] for n in (1,2,3,4,17,25,97)]==[
    False,True,True,False,True,False,True]

  print("\n== Сортировка выбором и бинарный поиск ==")
  sample,_=selection_sort(MEASUREMENTS)
  print("Исходный:",MEASUREMENTS)
  print("Отсортированный:",sample)
  assert sample==[7,9,11,12,15,15,18,18,18,21]
  assert MEASUREMENTS[0]==12  # исходный список не изменён

  print("\n== Сравнение числа сравнений ==")
  header=(f"{'n':>5} | {'линейный ср.':>12} | {'линейный худш.':>14} | "
          f"{'бинарный ср.':>12} | {'бинарный худш.':>14} | {'сорт. выбором':>13}")
  print(header)
  for n,lin_avg,lin_worst,bin_avg,bin_worst,sort_cmp in compare_searches():
    print(f"{n:>5} | {lin_avg:>12.2f} | {lin_worst:>14} | "
          f"{bin_avg:>12.2f} | {bin_worst:>14} | {sort_cmp:>13}")
