class cNoSimples:
	#Classe de nó com apenas referência para o próximo item, para ser utilizado em uma lista simplesmente encadeada.
	def __init__(self, dado):
		self.dado = dado
		self.prox = None

	def getDado(self):
		#Função que retorna o dado armazenado pelo nó.
		return self.dado

	def setDado(self, dado):
		#Função que altera o dado armazenado no nó.
		self.dado = dado

	def setProx(self, proximo):
		#Função que determina o nó seguinte ao atual.
		self.prox = proximo

	def getProx(self):
		#Função que retorna o nó seguinte ao atual.
		return self.prox

	def __str__(self):
		#A função str retorna a conversão em string do dado armazenado no nó.
		return str(self.dado)