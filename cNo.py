class cNo:
	#Classe que implementa o TAD nó para ser utilizado nas listas encadeadas.
	def __init__(self, dado = None):
		#Função construtora do nó. Como utilizaremos uma lista duplamente encadeada, o nó precisa ter três atributos: o dado que o nó vai armazenar; o nó anterior; e o próximo nó.
		#A função recebe o dado que será armazenado como parâmetro, mas se a função não receber nenhum dado, ela irá, por padrão, armazenar None no lugar do dado.
		self.dado = dado
		self.prev = None
		self.prox = None

	def getDado(self):
		#Função que retorna o dado armazenado pelo nó.
		return self.dado

	def setDado(self, dado):
		#Função que altera o dado armazenado no nó.
		self.dado = dado

	def getPrev(self):
		#Função que retorna o nó anterior ao atual.
		return self.prev

	def getPrevX(self, x):
		#Função que retorna o nó localizado x "casas" antes do nó atual
		noAtual = self
		i = 0
		while i < x:
			if noAtual.prev != None:
				noAtual = noAtual.prev
			else:
				raise IndexError("Tentativa de acesso a um elemento anterior ao primeiro elemento da lista")
			i += 1
		return noAtual
	
	def setPrev(self, anterior):
		#Função que determina o nó anterior ao atual.
		self.prev = anterior
		self.prev.prox = self

	def getProx(self):
		#Função que retorna o nó seguinte ao atual.
		return self.prox

	def getProxX(self, x):
		#Função que retorna o nó localizado x "casas" depois do nó atual
		noAtual = self
		i = 0
		while i < x:
			if noAtual.prox != None:
				noAtual = noAtual.prox
			else:
				raise IndexError("Tentativa de acesso a um elemento posterior ao último elemento da lista")
			i += 1
		return noAtual

	def setProx(self, proximo):
		#Função que determina o nó seguinte ao atual.
		self.prox = proximo
		self.prox.prev = self

	def __str__(self):
		#Função que define como a instância da classe cNo deve ser convertida para string
		#Retorna uma string contendo o dado armazenado pelo Nó.
		return str(self.dado)

	#Operadores de comparação:
	#Define como nós devem ser comparados.
	#Nós queremos que apenas os dados dos nós sejam comparados, então vamos apenas definir que comparar nós significa que estamos na verdade comparando os dados que eles armazenam.
	def __lt__(self, other):
		#Define como o operador "<" (menor que) funciona para comparar nós.
		return self.dado < other.dado

	def __gt__(self, other):
		#Define como o operador ">" (maior que) funciona para comparar nós.
		return self.dado > other.dado

	def __le__(self,other):
		#Define como o operador "<=" (menor ou igual a) funciona para comparar nós.
		return self.dado <= other.dado

	def __ge__(self,other):
		#Define como o operador ">=" (maior ou igual a) funciona para comparar nós.
		return self.dado >= other.dado

	def __eq__(self,other):
		#Define como o operador "==" (igual a) funciona para comparar nós.
		try:
			return self.dado == other.dado
		except:
			#Caso não seja possível realizar a comparação entre os dados, entende-se que eles são de tipos diferentes, portanto não são iguais.
			return False

	def __ne__(self, other):
		#Define como o operador "!=" (diferente de) funciona para comparar nós.
		try:
			return self.dado != other.dado
		except:
			#Caso não seja possível realizar a comparação entre os dados, entende-se que eles são de tipos diferentes, portanto não são iguais.
			return True