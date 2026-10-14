student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10

print('Крайние символы имени:',student[0],student[3])
print(f'Имя и фамилия: {student[:4]}, {student[5:]}')
print(f'Регистры: {student.upper()}, {student.lower()}')
print(f'Инициалы: {student[0]}. {student[5]}.')
print('Курс наоборот:',course[::-1])
percent=completed/total*100
print("%s — %s: %s/%s (%s%%)"%(student,course,completed,total,percent))
print("{} — {}: {}/{} ({}%)".format(student,course,completed,total,percent))
print(f"{student} — {course}: {completed}/{total} ({percent}%)")

symbol="Я"
print(f'{symbol = }')
print(f'{ord(symbol) = }')
print(f'{chr(ord(symbol)) = }')
print(f'{symbol.encode('utf-8') = }')
print(f'{len(symbol.encode('utf-8')) = }')

#student[0]='O'