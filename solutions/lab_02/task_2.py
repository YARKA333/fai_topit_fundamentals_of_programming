import copy

original=[["Python",5],["Algorithms",4]]
alias=original
shallow=original.copy()
deep=copy.deepcopy(original)

def show(stage):
  print(f"\n{stage}")
  for name,value in (("original",original),("alias",alias),("shallow",shallow),("deep",deep)):
    print(f"{name}: {value}; id внешнего={id(value)}; id первого вложенного={id(value[0])}; id оценки={id(value[0][1])}")

show("Исходное состояние")
original.append(["Databases",5])
show("После original.append")
original[0][1]=3
show("После original[0][1]=3")

print("\nМатрицы")

wrong_matrix=[[0]*3]*3
wrong_matrix[0][0]=1
print("wrong_matrix:",wrong_matrix)
print("id строк wrong:",[id(row) for row in wrong_matrix])


correct_matrix=[[0]*3 for _ in range(3)]
correct_matrix[0][0]=1
print("correct_matrix:",correct_matrix)
print("id строк correct:",[id(row) for row in correct_matrix])

assert wrong_matrix[0] is wrong_matrix[1]
assert correct_matrix[0] is not correct_matrix[1]
assert deep==[["Python",5],["Algorithms",4]]
