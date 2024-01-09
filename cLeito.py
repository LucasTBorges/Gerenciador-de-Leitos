from random import randint
import cLista
from math import sin


class cLeito:
    def __init__(self, registros = cLista.cLista()):
        #A função contrutora recebe uma lista com os registros de todos os leitos disponíveis para evitar a geração de dois leitos com o mesmo id, que seria posteriormente utilizado para localizar o
        #leito que o paciente deve ser enviado.

        #Uma instância da classe leito tem dois atributos:

        #Idade
        #A faixa etária a qual o leito é destinada. (0 para Neonatal, 1 para pediátrico e 2 para adulto.)
        #Como a probabilidade de que um paciente seja de uma determinada faixa etária é diferente para cada faixa etária, o peso da distribuição de leitos tambem deve ser diferente.
        #Utiliza os mesmos pesos da geração de pacientes.
        self.idade = randint(0, 5)
        if self.idade > 2:
            #Se a chave gerada é um número de 3 a 5, o leito é destinado a adultos
            self.idade = 2
        elif self.idade > 0:
            #Se a chave gerada é 1 ou 2, o leito é destinado a crianças
            self.idade = 1
        else:
            #Se a chave gerada é 0, o leito é destinado a bebês.
            self.idade = 0

        #Registro:
        #Um código numérico de 9 dígitos. Os 3 primeiros representando o ID do hospital em que está localizado, os 5 seguintes representando um código aleatório, e o último dígito representando a
        #faixa etária destinada ao uso do leito (0 para Neonatal, 1 para pediátrico e 2 para adulto.)
        #Para essa simulação, imaginaremos um conjunto universo de 100 hospitais diferentes
        codigo = randint(0, 99999999)
        self.registro = codigo * 10 + self.idade
        while self.registro in registros:
            codigo = randint(0, 99999999)
            self.registro = codigo * 10 + self.idade

    def __str__(self):
        #Retorna uma string com o registro do leito (com os devidos zeros a esquerda adicionados).
        codigo = str(self.registro)
        zerosNum = 9 - len(codigo)
        output = ""
        for i in cLista.intervalo(zerosNum):
            output += '0'
        output += codigo
        return output

def gerar(registros, dia):
    #Retorna uma lista com até 8 leitos gerados aleatoriamente. Recebe como parâmetro os registros dos leitos sendo utilizados para evitar a duplicidade de IDs.
    #Recebe o dia da simulação para calcular o intervalo de quantidade de leitos possível segundo a fórmula explicada no relatório do projeto.
    output = cLista.cLista()
    media = (2 * sin(dia/2)) + 4
    max = round(media + 2)
    min = round(media - 2)
    max = int(max)
    min = int()
    for i in cLista.intervalo(randint(min,max)):
        output.inserir(cLeito(registros))
    return output