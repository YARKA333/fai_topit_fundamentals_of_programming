import sys
import tracemalloc

print("ЧАСТЬ 1. РАЗМЕРЫ ОБЪЕКТОВ")
values=list(range(10))
objects=[
  ("Пустой список",[]),
  ("Список из 10 чисел",values),
  ("Кортеж из 10 чисел",tuple(values)),
  ("Строка из 10 символов","abcdefghij"),
  ("Целое число",123456),
  ("None",None)
]
for name,obj in objects:
  print(f"{name}: {sys.getsizeof(obj)} байт")

print("\nЧАСТЬ 2. РОСТ СПИСКА")
items=[]
previous=sys.getsizeof(items)
print(f"len={len(items)} size={previous}")
for number in range(100):
  items.append(number)
  current=sys.getsizeof(items)
  if current!=previous:
    print(f"len={len(items)} size={current}")
    previous=current

def measure(factory):
  tracemalloc.start()
  numbers=factory()
  current,peak=tracemalloc.get_traced_memory()
  result={
    "count":len(numbers),
    "object_size":sys.getsizeof(numbers),
    "current_kb":current/1024,
    "peak_kb":peak/1024
  }
  tracemalloc.stop()
  return result

print("\nЧАСТЬ 3. TRACEMALLOC")
for name,factory in (("list(range(100_000))",lambda:list(range(100_000))),("range(100_000)",lambda:range(100_000))):
  result=measure(factory)
  print(f"{name}: элементов={result['count']}, размер внешнего объекта={result['object_size']} байт, текущая память={result['current_kb']:.2f} KiB, пик={result['peak_kb']:.2f} KiB")
print("Итог: list материализует все элементы, range хранит параметры последовательности.")
