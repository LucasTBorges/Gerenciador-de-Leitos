import cNoSimples

class cPilha:
    #Classe de lista simplesmente encadeada com apenas referência ao topo, seguindo a política LIFO (Last In First Out).
    def __init__(self):
        self.topo = None
        self.tamanho = 0

    def isVazio(self):
        #Retorna um valor booleneano indicando se a pilha está vazia.
        return self.tamanho == 0

    def __len__(self):
        return self.tamanho

    def inserir(self, dado):
        #Insere um novo nó no topo
        novoNo = cNoSimples.cNoSimples(dado)
        if self.isVazio():
            #Se a lista está vazia, simplesmente coloca o novo nó no topo.
            self.topo = novoNo
            self.tamanho += 1
        else:
            #Se a lista já possui ao menos um elemento, o coloca como segundo da pilha e insere o novo no topo.
            antigo = self.topo
            novoNo.setProx(antigo)
            self.topo = novoNo
            self.tamanho += 1

    def getTopo(self):
        #Retorna o dado armazenado no nó presente no topo da pilha.
        if not self.isVazio():
            return self.topo.getDado()
        return None

    def popTopo(self):
        #Remove o nó do topo da pilha e retorna o valor removido
        if not self.isVazio():
            descarte = self.topo
            self.topo = self.topo.getProx()
            self.tamanho -= 1
            return descarte.getDado()

    def __str__(self):
        #Retorna uma string com um nó por linha, do topo até o fim da pilha.
        output = ""
        noatual = self.topo
        while noatual is not None:
            output += f'{noatual}\n'
            noatual = noatual.getProx()
        return output