import sys
import tracemalloc

COUNT=100_000

def measure(name,factory):
  tracemalloc.start()
  values=factory()
  current,peak=tracemalloc.get_traced_memory()
  result={
    "name":name,
    "count":len(values),
    "object_size":sys.getsizeof(values),
    "current_kb":current/1024,
    "peak_kb":peak/1024
  }
  tracemalloc.stop()
  return result

results=[
  measure("Материализованный список",lambda:list(range(COUNT))),
  measure("Диапазон range",lambda:range(COUNT))
]
for result in results:
  print(f"{result['name']}: элементов={result['count']}; размер объекта={result['object_size']} байт; текущая память={result['current_kb']:.2f} KiB; пик={result['peak_kb']:.2f} KiB")
ratio=results[0]["peak_kb"]/results[1]["peak_kb"] if results[1]["peak_kb"] else float("inf")
print(f"Отношение пиков list/range: {ratio:.2f}")

