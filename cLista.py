import cNo

class cLista:
    #Classe de lista duplamente encadeada com referência ao início e fim.
    #Algumas das funções implementadas não chegaram a ser utilizadas, mas foram mantidas no código para fins de manter a generalidade e versatilidade do código, que pode facilmente ser reutilizado e repropositado.

    def __init__(self, ordem = False):
        #A função inicializadora possui uma chave pra indicar se a lista deve ser ordenada ou não. Chave mantida em False por padrão.
        #No caso de ser ordenada, ordenação é crescente. Ou seja, o menor valor aparece no início da lista.
        self.inicio = None
        self.fim = None
        self.ordenada = ordem

    def inserir(self, novoDado):
        #Cria um nó que guarda o novo dado e o insere no final da lista (no caso de ser uma lista desordenada) ou na sua devida posição (no caso de uma lista ordenada).
        novoNo = cNo.cNo(novoDado)
        if not self.isVazio():
            #Inserção quando a lista não está vazia
            if (not self.ordenada) or novoNo > self.fim:
                #Se a lista não for do tipo ordenada ou a inserção no final não quebrar a ordem da lista, a função irá simplesmente inserir o novo nó no final.
                if len(self) == 1:
                    #Se só tiver um elemento na lista, tanto a referência ao fim quanto ao começo estarão apontando pro mesmo nó. Então precisaremos lidar com isso o inserindo no final e o ligando com o início.
                    self.fim = novoNo
                    self.inicio.setProx(self.fim)
                    return
                self.fim.setProx(novoNo)
                self.fim = novoNo
            else:
                #Se a lista for do tipo ordenada, o elemento será inserido em sua posição correta.
                if len(self) == 1:
                    #Se só tiver um elemento na lista, tanto a referência ao fim quanto ao começo estarão apontando pro mesmo nó. Então precisaremos lidar com isso da seguinte forma:
                    if novoNo > self.inicio:
                        #Se o lugar do novo nó for no final, o colocaremos no final e o ligaremos ao início.
                        self.fim = novoNo
                        self.inicio.setProx(self.fim)
                        return
                    else:
                        #Caso contrário, o colocaremos no início e o ligaremos ao final.
                        self.inicio = novoNo
                        self.inicio.setProx(self.fim)
                        return
                predecessor = self.fim
                while predecessor is not None:
                    #A função vai retornando do fim enquanto não chegar no início ou encontrar a posição correta do novo nó.
                    if novoNo < predecessor:
                        predecessor = predecessor.getPrev()
                    else:
                        break
                if predecessor is None:
                    #Se a função encontrar o início antes de encontrar a posição ideal do novo nó, ele será inserido no início.
                    self.inicio.setPrev(novoNo)
                    self.inicio = novoNo
                else:
                    #Se a posição for encontrada, o nó será inserido na posição correta, o ligando com os dois nós que o antecede e sucede.
                    sucessor = predecessor.getProx()
                    predecessor.setProx(novoNo)
                    if sucessor is not None:
                        sucessor.setPrev(novoNo)
        else:
            #Inserção quando a lista está vazia.
            self.inicio = novoNo
            self.fim = self.inicio

    #As próximas duas funções definem como iterar por uma instância de uma classe, possibilitando o uso de operadores como o "in", destinados a tipos iteráveis de objeto.
    def __iter__(self):
        self.noAtual = self.inicio
        return self

    def __next__(self):
        #Para iterar um objeto, o Python pega os retornos da função next até que o erro StopIteration seja lançado, que aqui acontece quando o próximo nó é "None". Ou seja, quando á iteração chega np último nó.
        if self.noAtual is not None:
            iteracao = self.noAtual
            self.noAtual = self.noAtual.prox
            return iteracao
        else:
            del self.noAtual
            raise StopIteration

    def __len__(self):
        tamanho = 0
        atualNo = self.inicio
        while atualNo is not None:
            atualNo = atualNo.getProx()
            tamanho += 1
        return tamanho

    def isVazio(self):
        #Retorna um boolean que indica se a lista está vazia.
        return len(self) == 0

    def popInicio(self):
        #Para situações em que a lista deve se comportar segundo a política FIFO (First In First Out). Remove o primeiro dado da lista e retorna o dado armazenado pelo nó removido.
        if not self.isVazio():
            dado = self.inicio.getDado()
            descarte = self.inicio
            self.inicio = self.inicio.getProx()
            if self.inicio is not None:
                self.inicio.prev = None
            del descarte
            if self.isVazio():
                #Se o item era único da lista, e portanto, também estava sendo referenciado por self.fim, remove a referência. 
                self.fim = None
            return dado

    def getInicio(self):
        #Retorna o dado armazenado no nó do início da lista.
        if not self.isVazio():
            return self.inicio.getDado()
        return None

    def __getitem__(self, indice):
        #Permite o acesso a dados armaenados nos nós da lista pelo índice do nó utilizando a notação lista[índice].
        #Para maior eficiência, a função determina se o nó buscado está mais perto do início ou no fim da lista e, baseado nisso, "escolhe" se vale mais a pena buscar o nó começando pelo inicio e "andando" pra frente ou
        #começando pelo fim e "andando" pra trás, dessa forma reduzindo o pior caso e o caso médio de execução do código pela metade.
        if self.isVazio():
            raise IndexError("Tentiva de acesso a item numa lista vazia.")
        indiceMax = len(self) - 1
        if indice > indiceMax:
            raise IndexError("Índice fora do alcance da lista.")
        if indice<0:
            raise IndexError("Tentativa de acesso a um índice negativo")
        if indice <= indiceMax//2:
            #Caso o nó esteja na primeira metade da lista, a função começa no início e vai lendo pra frente.
            noAtual = self.inicio
            i = 0
            while i!=indice:
                noAtual = noAtual.getProx()
                i += 1
            return noAtual
        #Caso o nó esteja na segunda metade da lista, a função começa no final e vai lendo pra trás.
        noAtual = self.fim
        i = 0
        while i != indiceMax - indice:
            noAtual = noAtual.getPrev()
            i+= 1
        return noAtual

    def buscar(self, dado):
        #Retorna uma referência para nó que armazena a primeira ocorrência do dado.
        for i in self:
            if i.getDado() == dado:
               return i
        #Caso a função não encontre o dado informado, ela resultará em um erro.
        raise KeyError(f'"{dado}" não encontrado na lista.')

    def remover(self, no):
        #Remove o nó da lista que está no índice correspondente, o nó correspondente (caso o parâmetro inserido seja um nó), ou a primeira instância do valor inserido caso o valor não seja nem um inteiro nem um nó.
        indice = -1
        if isinstance(no, int):
            descarte = self[no]
            indice = no
        elif isinstance(no, cNo.cNo):
            descarte = no
        else:
            descarte = self.buscar(no)
        if descarte == self.inicio or indice == 0:
            #Se o nó removido é o primeiro, então a função popInicio() é chamada.
            self.popInicio()
            del descarte
            return
        elif descarte == self.fim or indice == len(self) - 1:
            #Se o nó removido é o último, então a função coloca o penúltimo nó no lugar do último e remove a ligação entre os dois.
            self.fim = self.fim.getPrev()
            self.fim.prox = None
            del descarte
            return
        else:
            #Se o nó removido estiver no meio da lista, ele é deletado e o nó anterior passa a apontar pro sucessor do nó removido e vice-versa.
            predecessor = descarte.getPrev()
            sucessor = descarte.getProx()
            predecessor.setProx(sucessor)
            del descarte
            return

    def limpar(self):
        #Esvazia a lista.
        for i in self:
            self.popInicio()

    def __del__(self):
        #Remove as referências a todos os nós e atributos da lista.
        self.limpar()
        del self.inicio
        del self.fim
        del self.ordenada

    def __str__(self):
        #Retorna uma string com os dados armazenados em cada nó, com uma quebra de linha entre eles.
        output = ""
        for i in self:
            if i is not self.fim:
                #Enquanto não estiver no último elemento, concatena ao output o dado do elemento atual e uma quebra de linha
                output += f'{i.getDado()}\n'
            else:
                #No último elemento, concatena apenas o seu dado, sem uma quebra de linha no final.
                output += str(i.getDado())
        return output


def intervalo(limite):
    #Função que retorna uma instância da classe cLista contendo n inteiros de 0 até n - 1. 
    lista = cLista()
    i = 0
    while i != limite:
        lista.inserir(i)
        i += 1
    return lista