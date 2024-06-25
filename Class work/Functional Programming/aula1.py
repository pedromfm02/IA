#Exercicio 1.1
def comprimento(lista):

	if lista == []:
		return 0

	return 1 + comprimento(lista[1:])


#Exercicio 1.2
def soma(lista):
	
	if lista == []:
		return 0

	return lista[0] + soma(lista[1:])

#Exercicio 1.3
def existe(lista, elem):

	if lista == []:
		return False	

	if lista[0] == elem:
		return True

	return existe(lista[1:], elem)


#Exercicio 1.4
def concat(l1, l2):
	if l1 == []:
		return l2
	if l2 == []:
		return l1
	
	l1.append(l2[0])

	return concat(l1, l2[1:])

#Exercicio 1.5
def inverte(lista):
	
	if lista == []:
		return []
	
	return concat([lista[-1]], inverte(lista[:-1]))

#Exercicio 1.6
def capicua(lista):
	
	if comprimento(lista) == 1 or lista == []:
		return True
	
	if lista[0] == lista[-1]:
		return capicua(lista[1:-1])
	
	return False

#Exercicio 1.7
def concat_listas(lista):
	if lista == []:
		return []
	
	return concat(lista[0],concat_listas(lista[1:]))

#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []:
		return []
	if lista[0] == original:
		return concat([novo], lista[1:])
	return concat ([lista[0]], substitui(lista[1:], original, novo))

#Exercicio 1.9
def fusao_ordenada(lista1, lista2):
	if lista1 == []:
		return lista2
	if lista2 == []:
		return lista1
	
	if lista1[0] < lista2[0]:
		return concat([lista1[0]], fusao_ordenada(lista1[1:], lista2))
	return concat([lista2[0]], fusao_ordenada(lista2[1:], lista1))

#Exercicio 1.10
def lista_subconjuntos(lista):
	pass


#Exercicio 2.1
def separar(lista):
	if lista == []:
		return [], []
	a,b = lista[0]

	la,lb = separar(lista[1:])

	return [a] + la, [b] + lb 

#Exercicio 2.2
def remove_e_conta(lista, elem):
	pass

#Exercicio 3.1
def cabeca(lista):
	pass

#Exercicio 3.2
def cauda(lista):
	pass

#Exercicio 3.3
def juntar(l1, l2):
	if len(l1) != len(l2):
		return None
    
	if l1 == []:
		return []
	
	return [(l1[0],  l2[0])] + juntar(l1[1:], l2[1:])

#Exercicio 3.4
def menor(lista):
	if lista == []:
		return None
	
	if len(lista) == 1:
		return lista[0]
	
	m = menor(lista[1:])
	if lista[0] < m:
		return lista[0]
	return m


#Exercicio 3.6
def max_min(lista):
	if lista == []:
		return None
	
	if len(lista) == 1:
		return lista[0], lista[0]
	
	M, m = max_min(lista[1:])

	if lista[0] > M:
		return lista[0] , M
	if lista[0] < m:
		return M, lista[0]
	
	return M, m
