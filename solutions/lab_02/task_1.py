from copy import deepcopy

print("ЭКСПЕРИМЕНТ A: неизменяемый объект")
a=10
b=a
print("До:",a,b,"id:",id(a),id(b))
a+=1
print("После a+=1:",a,b,"id:",id(a),id(b))
assert b==10 and a==11

print("\nЭКСПЕРИМЕНТ B: изменяемый объект")
first=[10,20]
second=first
print("До изменения:",first,second,"id:",id(first),id(second))
second.append(30)
print("После append:",first,second,"id:",id(first),id(second))
assert first is second and first==[10,20,30]

second=[10,20,30]
print("После переназначения second:",first,second)
print("==:",first==second,"is:",first is second)
second.append(40)
print("После изменения нового списка:",first,second)
assert first==[10,20,30] and second==[10,20,30,40]

print("\nПРАКТИЧЕСКАЯ ЗАДАЧА: конфигурации")
config_a={
  "name":"Учебный проект A",
  "participants":["Аня","Борис"],
  "launch":[["--debug"],["--port","8000"]]
}
config_alias=config_a
config_alias["participants"].append("Вера")
config_alias["launch"][0].append("--verbose")
print("После изменения алиаса:")
print("A:",config_a)
print("Alias:",config_alias)
assert config_a is config_alias

config_b=deepcopy(config_a)
config_b["name"]="Учебный проект B"
config_b["participants"].append("Глеб")
config_b["launch"][0].append("--safe")
print("После независимого копирования и изменения:")
print("A:",config_a)
print("B:",config_b)
assert config_a is not config_b
assert config_a["participants"] is not config_b["participants"]
assert config_a["launch"] is not config_b["launch"]
assert "Глеб" not in config_a["participants"]
