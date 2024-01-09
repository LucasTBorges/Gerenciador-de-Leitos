import cNo
import cNoSimples
import cLista
import cPilha
import random
import cHumano
import cLeito
from sys import exit
import os

#O programa tentará importar a biblioteca colorama. Se não for possível, o programa será adaptado de acordo.
try:
    import colorama
    from colorama import Fore, Style
except:
    print('A biblioteca "Colorama" não foi encontrada. O programa será executado normalmente, com exceção da funcionalidade de imprimir os registros dos pacientes da cor correspondente ao seu código de emergência.')

#Função que habilitará o funcionamento do módulo colorama em dispositivos Windows (caso o módulo colorama esteja instalado):
try:
    colorama.just_fix_windows_console()
except:
    pass

def limparPrints():
    #Função que tentar limpar o terminal, utilizando o comando apropriado para o sistema operacional em que o programa está sendo executado (Windows ou Linux).
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("Não foi possível limpar o terminal.")

def codigo(codigo):
    #Retorna uma string contendo o nome do código de emergência correspondente
    if codigo == 4:
        return "Código Vermelho (Emergência)"
    if codigo == 3:
        return "Código Laranja (Muito Urgente)"
    if codigo == 2:
        return "Código Amarelo (Urgente)"
    if codigo == 1:
        return "Código Verde (Pouco Urgente)"
    if codigo == 0:
        return "Código Azul (Não Urgente)"

def ala(faixaetaria):
    #Retorna uma string contendo o nime da ala correspondente ao código de faixa etária inserido.
    if faixaetaria == 0:
        return "Ala Neonatal"
    if faixaetaria == 1:
        return "Ala Pediátrica"
    if faixaetaria == 2:
        return "Ala Adulta"

def morte(humano):
    #Retorna uma string descrevendo a morte de um paciente.
    return (f'O paciente de registro {humano} faleceu na {ala(humano.idade)}.\n')

def flutuacao(humano, codigoantigo):
    #Retorna uma string descrevendo a mudança de código de prioridade de um paciente.
    if humano.prioridade() == codigoantigo:
        return ""
    if humano.prioridade() >= 2:
        return (f'O paciente de registro {humano}, da {ala(humano.idade)}, mudou de código de prioridade, que antes era {codigo(codigoantigo)}, e agora está no {codigo(humano.prioridade())}\n')
    else:
        return (f'O paciente de registro {humano}, da {ala(humano.idade)}, mudou de código de prioridade, que antes era {codigo(codigoantigo)}, e agora está no {codigo(humano.prioridade())}. Portanto, não necessita mais de um leito na UTI e deixou a fila de espera.\n')

def atendimento(humano, leito):
    #Retorna uma string descrevendo o encaminhamento do paciente para o leito.
    return(f'O paciente de registro {humano}, da {ala(humano.idade)}, foi encaminhado para o leito de registro {leito}.\n')
def printcolor(humano):
    #Imprime o registro de um paciente da cor do seu código de prioridade (exceto os de código laranja, que são impressos em magenta)
    try:
        if humano.prioridade() == 4:
            print(Fore.RED + str(humano), Style.RESET_ALL)
        elif humano.prioridade() == 3:
            print(Fore.MAGENTA + str(humano), Style.RESET_ALL)
        elif humano.prioridade() == 2:
            print(Fore.YELLOW + str(humano), Style.RESET_ALL)
        elif humano.prioridade() == 1:
            print(Fore.GREEN + str(humano), Style.RESET_ALL)
        elif humano.prioridade() == 0:
            print(Fore.CYAN + str(humano), Style.RESET_ALL)
    except:
        print(humano)


#Filas pra cada faixa etára:
neonatal = cLista.cLista(True)
pediatrico = cLista.cLista(True)
adulto = cLista.cLista(True)

#Pilhas de leitos para cada faixa etária:
leitos_neonatal = cPilha.cPilha()
leitos_pediatrico = cPilha.cPilha()
leitos_adulto = cPilha.cPilha()

#Armazenamento de ids existentes para evitar a duplicidade (os registros devem ser únicos).
ids_pacientes = cLista.cLista()
ids_leitos = cLista.cLista()

#Contador de dias desde o dia 0
dia = 0

#Armazenamento da quantidade de dias extras que devem se passar:
ciclos = 0

#Quantidade máxima de pacientes gerados por dia:
maxpacientes = 8

#Número de Mortos
mortos = 0

#Pacientes Atendidos
atendidos = 0

#Pacientes que Melhoraram
melhoraram = 0

print("As cores dos registros representam o código de emergência do paciente. Com exceção do código Laranja, que é representado pela cor magenta, todos são representado por suas respectivas cores.")
maxpacientes_novo = input("Insira um número para ser a quantidade máxima de pacientes gerados no dia (leve em conta que são gerados um máximo de 8 leitos por dia): ")
try:
    maxpacientes = abs(int(maxpacientes_novo))
except:
    print("Parece que houve um problema configurando a quantidade máxima de pacientes com o valor inserido. Máximo de pacientes definido para o valor padrão (8).")
while True:
    #O ciclo de um dia na simulação:
    ciclos -= 1
    if ciclos <= 0:
        ciclos = 0
        comando = input(f'Submeta qualquer entrada (ou aperte enter) para apagar o dia anterior (caso exista) e iniciar a simulação do dia {dia}, ou "sair" para encerrar o programa. Insira um inteiro n para avançar n dias. ')
        try:
            ciclos = abs(int(comando))
        except:
            if comando == "sair":
                exit()
    limparPrints()
    print(f'Simulando dia {dia}...')
    mudancas = ""
    #Novos humanos serão aleatoriamente gerados e entrarão na simulação.
    print("Gerando novos pacientes...")
    novoshumanos = cHumano.gerar(dia, ids_pacientes, maxpacientes)
    idade0 = 0
    idade1 = 0
    idade2 = 0
    for i in novoshumanos:
        humano = i.getDado()
        if i.getDado().idade == 0:
            idade0 += 1
            neonatal.inserir(humano)
            ids_pacientes.inserir(humano.registro)
        elif i.getDado().idade == 1:
            idade1 += 1
            pediatrico.inserir(humano)
            ids_pacientes.inserir(humano.registro)
        else:
            idade2 += 1
            adulto.inserir(humano)
            ids_pacientes.inserir(humano.registro)
    mudancas += f'Chegaram {len(novoshumanos)} novos pacientes.\nDestes, {idade0} da Ala Neonatal, {idade1} da Ala Pediátrica e {idade2} da Ala Adulta.\n'

    #Chegam novos leitos
    print("Gerando novos leitos...")
    novosleitos = cLeito.gerar(ids_leitos, dia)
    idade0 = 0
    idade1 = 0
    idade2 = 0
    for i in novosleitos:
        leito = i.getDado()
        if leito.idade == 0:
            idade0 += 1
            leitos_neonatal.inserir(leito)
            ids_leitos.inserir(leito.registro)
        elif leito.idade == 1:
            idade1 += 1
            leitos_pediatrico.inserir(leito)
            ids_leitos.inserir(leito.registro)
        else:
            idade2 += 1
            leitos_adulto.inserir(leito)
            ids_leitos.inserir(leito.registro)
    mudancas += f'Foram liberados {len(novosleitos)} novos leitos.\nDestes, {idade0} da Ala Neonatal, {idade1} da Ala Pediátrica e {idade2} da Ala Adulta.\n\n'

    #Os pacientes são encaminhados aos leitos disponíveis e compatíveis com sua faixa etária
    print("Enviando pacientes para os leitos disponíveis...")
    for i in cLista.intervalo(len(leitos_neonatal)):
        if neonatal.isVazio():
            break
        paciente = neonatal.popInicio()
        leito = leitos_neonatal.popTopo()
        mudancas += atendimento(paciente, leito)
        atendidos += 1
        registro = paciente.registro
        ids_pacientes.remover(ids_pacientes.buscar(registro))
        ids_leitos.remover(ids_leitos.buscar(leito.registro))
    for i in cLista.intervalo(len(leitos_pediatrico)):
        if pediatrico.isVazio():
            break
        paciente = pediatrico.popInicio()
        leito = leitos_pediatrico.popTopo()
        mudancas += atendimento(paciente, leito)
        atendidos += 1
        registro = paciente.registro
        ids_pacientes.remover(ids_pacientes.buscar(registro))
        ids_leitos.remover(ids_leitos.buscar(leito.registro))
    for i in cLista.intervalo(len(leitos_adulto)):
        if adulto.isVazio():
            break
        paciente = adulto.popInicio()
        leito = leitos_adulto.popTopo()
        mudancas += atendimento(paciente, leito)
        atendidos += 1
        registro = paciente.registro
        ids_pacientes.remover(ids_pacientes.buscar(registro))
        ids_leitos.remover(ids_leitos.buscar(leito.registro))

    #Os pacientes sofrem as flutuações de um dia de espera na fila
    print("Simulando as flutuações de condição dos pacientes na fila de espera...")
    reinseridos = cLista.cLista()
    for i in neonatal:
        codigoinicial = i.getDado().prioridade()
        eventos = i.getDado().evento()
        if not i.getDado().isMal():
            mudancas += flutuacao(i.getDado(), codigoinicial)
            ids_pacientes.remover(ids_pacientes.buscar(i.getDado().registro))
            neonatal.remover(i)
            melhoraram += 1
        elif not i.getDado().isVivo():
            mortos += 1
            mudancas += morte(i.getDado())
            neonatal.remover(i)
        elif codigoinicial != i.getDado().prioridade():
            mudancas += flutuacao(i.getDado(), codigoinicial)
            neonatal.remover(i)
            reinseridos.inserir(i.getDado())

    for i in pediatrico:
        codigoinicial = i.getDado().prioridade()
        eventos = i.getDado().evento()
        if not i.getDado().isMal():
            mudancas += flutuacao(i.getDado(), codigoinicial)
            ids_pacientes.remover(ids_pacientes.buscar(i.getDado().registro))
            pediatrico.remover(i)
            melhoraram += 1
        elif not i.getDado().isVivo():
            mortos += 1
            mudancas += morte(i.getDado())
            pediatrico.remover(i)
        elif codigoinicial != i.getDado().prioridade():
            mudancas += flutuacao(i.getDado(), codigoinicial)
            pediatrico.remover(i)
            reinseridos.inserir(i.getDado())

    for i in adulto:
        codigoinicial = i.getDado().prioridade()
        eventos = i.getDado().evento()
        if not i.getDado().isMal():
            mudancas += flutuacao(i.getDado(), codigoinicial)
            ids_pacientes.remover(ids_pacientes.buscar(i.getDado().registro))
            adulto.remover(i)
            melhoraram += 1
        elif not i.getDado().isVivo():
            mortos += 1
            mudancas += morte(i.getDado())
            adulto.remover(i)
        elif codigoinicial != i.getDado().prioridade():
            mudancas += flutuacao(i.getDado(), codigoinicial)
            adulto.remover(i)
            reinseridos.inserir(i.getDado())

    for i in reinseridos:
        #Os pacientes que foram removidos das filas por trocarem de código de prioridade serão inseridos novamente na sua nova posição.
        if i.getDado().idade == 0:
            neonatal.inserir(i.getDado())
        elif i.getDado().idade == 1:
            pediatrico.inserir(i.getDado())
        else:
            adulto.inserir(i.getDado())

    #O estado atual do sistema é impresso no terminal.
    print("")
    print(f'Estado da simulação ao final do dia {dia}:\n')
    print(f'Total de mortos: {mortos}')
    print(f'Total de vezes em que um paciente foi encaminhado para um leito: {atendidos}')
    print(f'Total de vezes em que um paciente melhorou durante a sua espera na fila a ponto de não precisar mais de um leito: {melhoraram}')
    print("")
    print(f'Pacientes da Ala Neonatal aguardando um leito ({len(neonatal)} pacientes):')
    for i in neonatal:
        printcolor(i.getDado())
    print("")
    print(f'Pacientes da Ala Pediátrica aguardando um leito ({len(pediatrico)} pacientes):')
    for i in pediatrico:
        printcolor(i.getDado())
    print("")
    print(f'Pacientes da Ala Adulta aguardando um leito ({len(adulto)} pacientes):')
    for i in adulto:
        printcolor(i.getDado())
    print("")
    print(f'Leitos para pacientes da Ala Neonatal disponíveis ({len(leitos_neonatal)} leitos):')
    print(leitos_neonatal)
    print("")
    print(f'Leitos para pacientes da Ala Pediátrica disponíveis ({len(leitos_pediatrico)} leitos):')
    print(leitos_pediatrico)
    print("")
    print(f'Leitos para pacientes da Ala Adulta disponíveis ({len(leitos_adulto)} leitos):')
    print(leitos_adulto)
    print("")

    #As mudanças que ocorreram no dia são impressas.
    print(f'Mudanças que ocorreram no dia {dia}:\n')
    print(mudancas)
    dia += 1