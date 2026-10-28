import sys
import weakref

print("ПОДСЧЕТ ССЫЛОК")
data=[1,2,3]
print("После создания:",sys.getrefcount(data))
alias=data
print("После создания alias:",sys.getrefcount(data))
container=[data]
print("После помещения в контейнер:",sys.getrefcount(data))
del alias
print("После del alias:",sys.getrefcount(data))
container.clear()
print("После очистки контейнера:",sys.getrefcount(data))

print("\nСЛАБАЯ ССЫЛКА")
class Record:
  pass

record=Record()
weak_record=weakref.ref(record)
print("До удаления сильной ссылки:",weak_record())
del record
print("После удаления сильной ссылки:",weak_record())
assert weak_record() is None

print("\nWEAKVALUEDICTIONARY")
registry=weakref.WeakValueDictionary()

first=Record()
second=Record()

registry["first"]=first
registry["second"]=second
registry["temporary"]=Record()

print("После регистрации:",list(registry.keys()))
assert "temporary" not in registry

del first
print("После удаления first:",list(registry.keys()))
assert "first" not in registry and "second" in registry

del second
print("После удаления second:",list(registry.keys()))
assert len(registry)==0
