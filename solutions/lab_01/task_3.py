import math

print('\nA')

x=17
y=5.0

print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x // y)
print(x % y)
print(x ** y)

print('\nB')

print(2**1000)

print('\nC')

result=.1+.2
print(result)
print(result==.3)
print(result-.3)
print(math.isclose(result,.3))


print('\nD')

print(int("42"))
print(float("3.14"))
print(str(2026))
print(bool(0))
print(bool(-1))
print(bool(""))
print(bool("False"))
c=complex(2, -3)
print(c)
print(c.real,c.imag)