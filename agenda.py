import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  
  print(cor + texto + RESET)
  
# Funções de verificação - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Valida a prioridade.
def prioridadeValida(pri):
  ehPrioridadeValida = False
  if len(pri) == 3:                                          # Possui 3 caracteres?
    if pri[0] == "(" and pri[2] == ")":
      if pri[1].upper() >= "A" and pri[1].upper() <= "Z":    # Segundo caractere é uma letra?
        ehPrioridadeValida = True
  return ehPrioridadeValida


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else: # Validando os dígitos
    ehHoraValida = False
    hora = int(horaMin[0:2])
    minuto = int(horaMin[2:])
    if hora >= 0 and hora < 24:
      if minuto >= 0 and minuto < 60:
        ehHoraValida = True
    return ehHoraValida

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
   if len(data) != 8 or not soDigitos(data):
    return False
   else:
    ehDataValida = False
    dia = int(data[0:2])
    mes = int(data[2:4])
    ano = int(data[4:])
    if dia > 0 and dia <= 31:       # Dia é válido?
      if mes > 0 and mes <= 12:     # Mês é válido?
        if mesesDoAno(dia,mes):
          ehDataValida = True
    return ehDataValida
  
#Verifica se o dia e mês digitado fazem sentido juntos
def mesesDoAno(dia,mes):
  fazSentido = False
  if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
    if dia > 0 and dia <= 31:
      fazSentido = True
  elif mes == 2:
    if dia > 0 and dia <= 28:
      fazSentido = True
  else:
    if dia > 0 and dia <= 30:
      fazSentido = True
  return fazSentido

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) < 2 or proj[0] != "+":
    return False
  else:
    return True
  
# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
    if len(cont) < 2 or cont[0] != "@":
      return False
    else:
      return True

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True

# Utilizado para retirar o caractere de \n que venham como 'intrusos'
def retiraCaractereNovaLinha(lista):
  novaLista = []
  for l in lista:
    if l != "\n":
      novaLista = novaLista + [l.strip()]
  return novaLista

# Funções principais do Programa - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Ordena os elementos no formato dado por 'Organizar'
def ordenarPorPrioridade(lista):
  if lista == []:
    return []
  else:
    menor = []
    maior = []
    pivo = lista.pop(0)
    if pivo[1][2] == '': # Pivô é um espaço em branco
      maior = [x for x in lista if x[1][2] == '']
      menor = [y for y in lista if y[1][2] != '']
    else:
      maior = [y for y in lista if y[1][2] == '' or y[1][2][1] >= pivo[1][2][1]]
      menor = [x for x in lista if x[1][2] != '' and x[1][2][1] < pivo[1][2][1]]
    return ordenarPorPrioridade(menor) + [pivo] + ordenarPorPrioridade(maior)

# Função genérica que utiliza parâmetros para ordenar data - dia, mês, ano - e hora
# O parâmetro 'itens' é uma lista de tuplas
# O parâmetro 'tuplaPos' refere-se à posição desejada na tupla (posição0, posição1,posição2)
# O parâmetro 'elemento' refere-se à posição desejada dentro da tupla constante na posição 1
# Os parâmetros 'i' e 'f' são utilizados no slice para dividir as strings data e hora
def ordenaNumero(itens,tuplaPos,elemento,i,f):
  if itens == []:
    return []
  else:
    pivo = itens.pop(0)
    if pivo[tuplaPos][elemento] == '': # Pivô é um espaço em branco
      maior = [x for x in itens if x[tuplaPos][elemento] == '']
      menor = [y for y in itens if y[tuplaPos][elemento] != '']
    else:
      maior = [y for y in itens if y[tuplaPos][elemento] == '' or  int(y[tuplaPos][elemento][i:f]) >= int(pivo[tuplaPos][elemento][i:f])]
      menor = [x for x in itens if x[tuplaPos][elemento] != '' and int(x[tuplaPos][elemento][i:f]) < int(pivo[tuplaPos][elemento][i:f])]        
    return ordenaNumero(menor,tuplaPos,elemento,i,f) + [pivo] + ordenaNumero(maior,tuplaPos,elemento,i,f)

def ordenarPorDataHora(itens):
  prioridades = [] # Armazena quais são as prioridades constantes na lista 'itens'

  # 1º passo: Percorrer a lista 'itens' procurando quais são as prioridades constantes nela
  for i in itens:
    ultimo = i[1][2]
    if prioridades == [] or prioridades[len(prioridades)-1] != ultimo:
      prioridades.append(ultimo)
  # 2º passo: Criar pequenas listas de acordo com a prioridade dada (Uma lista só de A outra só de B...)
  listaDePrioridades = []
  for p in prioridades:
    listaDePrioridades.append([x for x in itens if p == str(x[1][2])])

  # 3º passo: Ordenar cada lista individualmente por dia
  listaAuxiliar = []
  for l in listaDePrioridades:
      listaAuxiliar += [ordenaNumero(l,1,0,0,2)]
  listaDePrioridades = listaAuxiliar

  # 4º passo: Ordenar cada lista individualmente por mês
  listaAuxiliar = []
  for l in listaDePrioridades:
      listaAuxiliar += [ordenaNumero(l,1,0,2,4)]
  listaDePrioridades = listaAuxiliar

  # 5º passo: Ordenar cada lista individualmente por ano
  listaAuxiliar = []
  for l in listaDePrioridades:
      listaAuxiliar += ordenaNumero(l,1,0,4,8)
  
  # print(listaAuxiliar)
  return listaAuxiliar


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.
#
# Recebe  uma lista
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras
    # Processa os tokens um a um, verificando se são as partes da atividade.
    for t in tokens:
      if t[0] == "+": # É um projeto
        if projetoValido(t):
          projeto = t
        else:
          desc = desc + t
      elif t[0] == "@": # É um contexto
        if contextoValido(t):
          contexto = t
        else:
          desc = desc + t
      elif t[0] == "(": # É uma prioridade
        if prioridadeValida(t):
          pri = '(' + t[1].upper() + ')'
        else:
          desc = desc + t
      elif soDigitos(t):# Pode ser data ou Hora
        if horaValida(t):# Testa se é hora
          hora = t
        else:
          if dataValida(t):
            data = t
          else:
            desc = desc + t
            desc = desc + ' '
      else: # É uma descrição
        desc = desc + t
        desc = desc + ' '
    itens.append((desc, (data, hora, pri, contexto, projeto)))
  return itens


# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  else:
    # Escreve no TODO_FILE. 
    try:
      novaAtividade = ''
      i = 0
      j = 0
      while i <= 5:
        if i != 3 and extras[j] != '':
          novaAtividade = novaAtividade + extras[j] + ' '
        elif i == 3:
          novaAtividade = novaAtividade + descricao + ' '
          j -= 1
        i += 1
        j += 1
      novaAtividade = novaAtividade + '\n'
      fp = open(TODO_FILE, 'a',encoding = "utf-8-sig")
      fp.write(novaAtividade)
      fp.close()
    except IOError as err:
      print("Não foi possível escrever para o arquivo " + TODO_FILE)
      print(err)
      return False
  return True

# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
   try:
      print('Itens Cadastrados:')
      print('\n')
      i = 1
      itemParaListar = []
      fp = open(TODO_FILE, 'r',encoding = "utf-8-sig")
      fpLista = fp.readlines()
      fpLista = retiraCaractereNovaLinha(fpLista)
      for item in fpLista:
        if i < 10:
          itemParaListar.append(organizar([item])[0] + ("00"+str(i),))
        else:
          itemParaListar.append(organizar([item])[0] + ("0"+str(i),))
        i += 1
      fp.close()
      itemParaListar = ordenarPorPrioridade(itemParaListar)
      itemParaListar = ordenarPorDataHora(itemParaListar)
      
      # Utilizo as variáveis com o objetivo de deixar o documento mais organizado no txt
      data = ''
      hora = ''
      pri  = ''
      ctx  = ''
      pro  = ''
      for item in itemParaListar:
        if item[1][0] == '': # Se a data for vazia
          data = '           '
        else:
          data = item[1][0][0:2]+"/"+item[1][0][2:4]+"/"+item[1][0][4:]
        if item[1][1] == '': # Se a hora foz vazia
          hora = '     '
        else:
          hora = item[1][1][0:2]+":"+item[1][1][2:]
        if item[1][2] == '':# Se a prioridade foz vazia
          pri = '   '
        else:
          pri = item[1][2]
        if item[1][3] == '':# Se o contexto for vazio
          ctx = '   '
        else:
          ctx = item[1][3]
        if item[1][4] == '':# Se a prioridade foz fazia
          pro = '   '
        else:
          pro = item[1][4]
        print(item[2],data,hora,pri,item[0],ctx,pro)
   except IOError as err:
      print("Não foi possível escrever para o arquivo " + TODO_FILE)
      print(err)

def fazer(num):
  r = remover(num)
  if r != False:
    fp = open(ARCHIVE_FILE,'a',encoding = "utf-8-sig")
    fp.write(r)
    fp.close()
  else:
    print('Erro ao processar o arquivo!') 

def remover(n):
  retirado = ()
  try:
    fp = open(TODO_FILE,'r',encoding = "utf-8-sig")
    arquivo = fp.readlines()
    arquivo = retiraCaractereNovaLinha(arquivo)
    if n <= len(arquivo):
      retirado = arquivo.pop(n-1)
    else:
      print("Linha inexistente!")
    fp.close()
    fp = open(TODO_FILE,'w',encoding = "utf-8-sig")
    for linha in arquivo:
      fp.write(linha + '\n')
    fp.close()
  except IOError as err:
      print("Não foi possível remover do arquivo " + TODO_FILE)
      print(err)
      return False
  return retirado
# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  try:
    fp = open(TODO_FILE,'r',encoding = "utf-8-sig")
    arquivo = fp.readlines()
    arquivo = retiraCaractereNovaLinha(arquivo)
    if num <= len(arquivo) and num >= 0:
      linha = organizar([arquivo[num-1]])[0]
      data = linha[1][0] + ' '
      hora = linha[1][1] + ' ' 
      pri  = prioridade + ' '
      desc = linha[0] + ' ' 
      ctx  = linha[1][3] + ' '
      proj = linha[1][4] + ' '
      arquivo[num-1] = data + hora + pri + desc + ctx + proj
      fp = open(TODO_FILE,'w',encoding = "utf-8-sig")
      for a in arquivo:
        a = a.strip()
        fp.write(a + '\n')
      # fp.writelines(arquivo)'''
      fp.close()
    else:
      print("Linha inexistente!")
  except IOError as err:
      print("Não foi possível remover do arquivo " + TODO_FILE)
      print(err)
      return False

# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos):
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    if adicionar(itemParaAdicionar[0], itemParaAdicionar[1]): # novos itens não têm prioridade
      print('Tarefa adicionada com sucesso!')
  elif comandos[1] == LISTAR:
    listar()
  elif comandos[1] == REMOVER:
    valor = comandos.pop()
    if remover(int(valor)) != False:
      print('Compromisso removido com sucesso!')
  elif comandos[1] == FAZER:
    num = comandos.pop()
    fazer(int(num))    
  elif comandos[1] == PRIORIZAR:
    prioridade = comandos.pop()
    num = comandos.pop()
    priorizar(int(num), "("+prioridade+")")    
  else :
    print("Comando inválido.")
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
