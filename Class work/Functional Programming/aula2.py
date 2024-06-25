import math

#Exercicio 4.1
impar = lambda n : n % 2 == 1

#Exercicio 4.2
positivo = lambda n : n > 0

#Exercicio 4.3
comparar_modulo = lambda x,y : abs(x) < abs(y)

#Exercicio 4.4
cart2pol = lambda x,y : (math.hypot(x,y), math.atan2(y,x))

#Exercicio 4.5
ex5 = lambda f, g, h: lambda x, y, z: h(f(x,y),g(y,z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    pass

#Exercicio 4.8
def subconjunto(lista1, lista2):
    pass

#Exercicio 4.9
def menor_ordem(lista, f):
    pass

#Exercicio 4.10
def menor_e_resto_ordem(lista, f):
    pass

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    pass
