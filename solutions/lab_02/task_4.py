import gc

print("СОСТОЯНИЕ СБОРЩИКА")
print("Автоматическая сборка включена:",gc.isenabled())
print("Пороги поколений:",gc.get_threshold())
print("Статистика поколений:",gc.get_stats())

print("\nЦИКЛ ИЗ ДВУХ СПИСКОВ")
first=[]
second=[]
first.append(second)
second.append(first)
first_id=id(first)
second_id=id(second)
print("first ссылается на second:",first[0] is second)
print("second ссылается на first:",second[0] is first)
del first
del second
collected=gc.collect()
print("Сохраненные id:",first_id,second_id)
print("Собрано объектов после удаления имен:",collected)

print("\nРУЧНАЯ СБОРКА ПРИ ОТКЛЮЧЕННОЙ АВТОМАТИЧЕСКОЙ")
was_enabled=gc.isenabled()
gc.disable()
before=gc.collect()
cycles=[]
for _ in range(5):
  left=[]
  right=[]
  left.append(right)
  right.append(left)
  cycles.append((left,right))
del cycles
manual=gc.collect()
print("Собрано до эксперимента:",before)
print("Собрано после удаления циклов:",manual)
if was_enabled:
  gc.enable()
print("Автоматическая сборка восстановлена:",gc.isenabled())
assert gc.isenabled()

print("\nГРАФ ИЗ СЛОВАРЕЙ")
independent={"name":"independent","links":[]}
a={"name":"A","links":[]}
b={"name":"B","links":[]}
c={"name":"C","links":[]}

a["links"].append(b)
b["links"].append(c)
c["links"].append(a)
print("A ->",a["links"][0]["name"],"B ->",b["links"][0]["name"],"C ->",c["links"][0]["name"])

independent_id=id(independent)

del a,b,c

graph_collected=gc.collect()
print("Собрано после удаления графа:",graph_collected)

assert id(independent)==independent_id and independent["name"]=="independent"
print("Независимый узел доступен:",independent)
