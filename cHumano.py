from cmath import isclose
import cNo
import cLista
import random

class cHumano:
	#Classe que representa um paciente de hospital.
	def __init__(self, chegada, registros = cLista.cLista()):
		#A função inicializadora recebe como parâmetro uma lista com os registros dos pacientes na fila do hospital, para evitar que seja gerado um paciente que compartilha o mesmo
		#registro do SUS que algum outro. Por padrão retorna uma lista vazia.

		#O paciente possuí 5 atributos: 
		
		#Registro SUS, um código numérico único de 9 dígitos gerado aleatoriamente para identificar o paciente;
		self.registro = random.randint(0, 999999999)
		codigo = cNo.cNo(self.registro)
		while codigo in registros:
			#Se já existir um paciente na lista com o código de registro do SUS, a função gera um novo código pro paciente até que seja um código único.
			self.registro = random.randint(0, 999999999)
			codigo = cNo.cNo(self.registro)

		#Coeficiente de risco, uma representação numérica da condição do paciente que segue uma escala de 0 a 99 (a partir de 100 o paciente está morto) que pode flutuar em quanto o paciente está na fila;
		#Quando o paciente chega na fila da UTI,é gerado um coeficiente de risco aleatório entre 40 e 98 segundo a fórmula explicada no relatório do projeto.
		#Realiza uma aproximação pra baixo do valor gerado.
		self.risco = round((((random.randint(0, 100))**2)/169)) + 40

		#Coeficiente de risco inicial;
		#Esse valor é o valor atribuído ao coeficiente de risco quando o paciente é gerado. Esse valor é imutável e é utilizado para calcular expressões baseadas na variação do coeficiente de risco desde que o paciente foi gerado.
		self.riscoinical = self.risco

		#Faixa Etária:
		#O paciente possui um número de 0 a 2 representando a faixa etária do paciente: 0 representando Neonatal, 1 representando Pediátrico, 2 representando Adulto. Esse valor não muda durante a estadia do paciente na fila.
		#Há um peso maior para a faixa adulta pois há um intervalo maior de idade que configura "Adulto", também por isso há um peso um pouco menor mas ainda maior que o Neonatal para o Pediátrico.
		self.idade = random.randint(0,5)
		if self.idade > 2:
			#Se o número gerado é de 3 a 5, o paciente é adulto.
			self.idade = 2
		elif self.idade > 0:
			#Se o número é 1 ou 2, o paciente é pediátrico.
			self.idade = 1
		#Se o número gerado não é nenhum dos citados acima, ele é zero. Ou seja, neonatal.

		#Dia de Chegada
		#O paciente possui um valor do tipo float que representa quando ele chegou na fila. A parte inteira representa o dia que o paciente chegou, e a parte fracionária o momento do dia que ele chegou.
		#Esse atributo é armazenado com o fim de ser utilizado como critério de ordenação na fila caso o paciente mude de código de prioridade devido a uma flutação na sua condição durante a sua espera por um leito.
		self.chegada = chegada

	def prioridade(self):
		#Retorna o código de emergência referente ao coeficiente de risco do paciente.
		if self.risco >= 80:
			#Se o coeficiente de risco é de 80 pra cima, retorna o código vermelho (Emergência), representado pelo número 4.
			return 4
		if self.risco >= 60:
			#Se o coeficiente de risco é de 60 pra cima, retorna o código laranja (Muito Urgente), representado pelo número 3.
			return 3
		if self.risco >= 40:
			#Se o coeficiente de risco é de 40 pra cima, retorna o código amarelo (Urgente), representado pelo número 2.
			return 2
		if self.risco >= 20:
			#Se o coeficiente de risco é de 20 pra cima, retorna o código verde (pouco urgente), representado pelo número 1.
			return 1
		#Se nenhum dos testes é cima se mostrou verdadeiro,retorna o código azul (não urgente), representado pelo número 0.
		return 0

	def flutuacao(self):
		#Retorna a diferença entre o coeficiente de risco inicial e atual.
		return self.riscoinical - self.risco

	def variacao(self):
		#Retorna a variação do coeficiente de risco, calculada a partir do módulo da diferença entre o coeficiente de risco inicial e atual.
		return abs(self.flutuacao())

	def isVivo(self):
		#Retorna True se o paciente está vivo e False caso contrário.
		return self.risco < 100

	def isMal(self):
		#Retorna False se o paciente ainda precisa de um leito na UTI (código amarelo pra cima) e False caso contrário.
		return self.risco >= 40

	def  __str__(self):
		#A função string retorna o registro do SUS do paciente com uma string (adicionando todos os devidos zeros a esquerda.)
		#Para calcular o número de zeros que devem ser adicionados, a função subtrai o número de dígitos do registro do paciente de 9 (o número máximo de dígitos)
		codigo = str(self.registro)
		zerosNum = 9 - len(codigo)
		output = ""
		for i in cLista.intervalo(zerosNum):
			output += '0'
		for i in codigo:
			output += i
		return output


	def evento(self):
		#Função que simula a flutuação de estado do paciente após um dia de espera na fila caso o paciente ainda esteja na fila (vivo e precisando de um leito na UTI).
		#Retorna as mudanças significativas (Melhora a ponto do paciente não precisar mais de um leito na UTI, morte do paciente e mudança do código de prioridade)
		if self.isVivo() and self.isMal():
			condicaoinicial = self.prioridade()
			mudoucodigo = False
			#Um número de 0 a 99 é gerado aleatoriamente para servir como base para decidir se haverá flutuação ou não.
			chave = random.randint(0,99)
			#A chance de flutuação é calculada com base na variação do estado do paciente até o momento, utilizando a fórmulada explicada no relatório do projeto.
			#Aproximação pra baixo realizada.
			flutuou = chave <= ((self.variacao() ** 2) // 110) + 20
			if flutuou:
				#Caso haja flutuação, um número de 0 a 99 é gerado aleatoriamente para servir como base para decidir se a flutuação será uma melhora ou piora.
				chave = random.randint(0, 99)
				#A chance de melhora é calculada com base na diferença entre o coeficiente de risco inicial e atual, utilizando a fórmulada explicada no relatório do projeto.
				#Aproximação pra baixo realizada.
				try:
					melhorou = chave <= ((self.flutuacao()**2)//350) * (self.variacao()//self.flutuacao()) + 20
				except:
					#Caso a variação seja zero, a chance deve ser de 20%. É necessário o uso de try/except pois nesse caso haverá uma divisão por zero na fórmula.
					melhorou = chave <= 20
				if melhorou:
					#Caso haja uma melhora, um valor aleatório entre 5 e 15 é diminuido do coeficiente de risco.
					self.risco -= random.randint(5,15)
				else:
					#Caso haja uma piora, um valor aleatório entre 5 e 15 é acrescentado ao coeficiente de risco.
					self.risco += random.randint(5,15)
				mudoucodigo = condicaoinicial != self.prioridade()
			#A variável "mudancas" vai guardar uma instância de cLista valores booleaneanos indicando se o paciente num código de prioridade de amarelo pra cima, se o paciente segue vivo e se 
			#o paciente mudou de código de prioridade (e portanto deve mudar de fila).
			mudancas = cLista.cLista()
			mudancas.inserir(self.isMal())
			mudancas.inserir(self.isVivo())
			mudancas.inserir(mudoucodigo)
			return mudancas
		else:
			#Se o paciente está morto ou não precisa de um leito, ele não deveria estar numa fila esperando por um leito e ter a função evento() aplicada nele.
			if not self.isVivo():
				raise RuntimeError("Tentativa de aplicação de evento num paciente morto.")
			elif not self.isMal():
				raise RuntimeError(f'Tentativa de aplicação de evento num paciente que não precisa de um leito na UTI, portanto não deveria estar na fila. Coeficiente de risco do paciente: {self.risco}')
			else:
				raise RuntimeError("Não deveria ser possível chegar nesse ponto do código.")

	#Operadores de comparação
	#Define como as instâncias de cHumano devem ser comparadas.
	#Como esses operadores seram utilizados para ordenar pacientes na fila, devemos utilizar o mesmo critério utilizado para ordenação: código de prioridade e hora de chegada.
	def __lt__(self, other):
		#Define como se comporta o operador < (menor que).
		if self.prioridade() != other.prioridade():
			return self.risco > other.risco
		return self.chegada < other.chegada

	def __gt__(self, other):
		#Define como se comporta o operador > (maior que).
		if self.prioridade() != other.prioridade():
			return self.risco < other.risco
		return self.chegada > other.chegada

	def __le__(self, other):
		#Define como se comporta o operador <= (menor ou igual a).
		return self < other or self.prioridade() == other.prioridade() and isclose(self.chegada,other.chegada)

	def __ge__(self, other):
		#Define como se comporta o operador >= (maior ou igual a).
		return self > other or self.prioridade() == other.prioridade() and isclose(self.chegada,other.chegada)

	#Comparadores de igualdade
	#Como estes não serão utilizados para ordenação, mas sim para busca, devemos usar o critério de identificação do paciente: o registro do SUS.
	def __eq__(self, other):
		#Define como se comporta o operador == (igual a).
		return self.registro == other.registro and self.registro == other.registro

	def __ne__(self,other):
		#Define como se comporta o operador != (diferente de).
		return not self == other

def gerar(dia, registros, max):
	#Retorna uma lista com 0 a x humanos que chegam no dia inserido como parâmetro, em momentos do dia diferentes. x sendo o valor máximo de pacientes inserido pelo usuário.
	novos = 0
	output = cLista.cLista()
	for i in cLista.intervalo(random.randint(0,max)):
		novos += 1
		#O "horário" de chegada é definido como a parte não inteira do valor que representa a chegada.
		horario = i.getDado()
		while horario >= 1:
			horario /= 10
		chegada = dia + horario
		output.inserir(cHumano(chegada, registros))
	return output