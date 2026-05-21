import sqlite3
import os

def exitfunc(n): #funcao de saida
    exit()

def clrScreen():
    try: os.system("cls")
    except: os.system("clear")

def ask_input(): # funcao para a entrada de linha
    temp=input(">")
    n=temp.split()
    return n

conf={
    "bdatual":"mydata.db",
    "numlista":5
}

def config(n):
    clrScreen()
    print(f'''========
SETTINGS
========
Banco de Dados Ativo: {conf["bdatual"]}
Numero de Resultados por Pagina: {conf["numlista"]}
========
Digite 'set db [nome_do_arquivo.db]' para mudar o banco de dados ativo;
Digite 'set num [numero]' para mudar o numero de resultados por pagina;
Digite 'exit' para voltar ao menu.''')
    while True:
        u=ask_input()
        try:
            if u[0]=="set":
                if u[1]=="db":
                    tempdb=u[2]
                    if ".db" not in u[2]:
                        tempdb=tempdb+".db"
                    conf.update({"bdatual":tempdb})
                    print(f"Banco de Dados Atual atualizado para {conf['bdatual']}")
                elif u[1]=="num":
                    tempnum=int(u[2])
                    if tempnum>0:
                        conf.update({"numlista":tempnum})
                        print(f"Numero de Resultados por Pagina atualizado para {conf['numlista']}")
                    else: print("Por favor, digite um numero maior que 0...")
                else: print("Por favor, digite um argumento valido...")
            elif u[0]=="exit": break
            else: print("Por favor, digite um comando valido...")
        except IndexError: print("Nao houveram argumentos suficientes para a sua operacao. Tente novamente...")
        except (ValueError,TypeError,OverflowError): print("O valor digitado nao corresponde a um inteiro ou possui valor invalido...")
    return 0

cmds={
    "add":1,
    "search":2,
    "import":3,
    "config":config,
    "help":5,
    "exit":exitfunc
}

erros={
    1:"aaaa"
}



def const_menu():
    clrScreen()
    print(f'''=========================
IT RISK MANAGER INTERFACE
=========================
Banco de Dados ativo: {conf["bdatual"]}
=========================
Digite 'add [tipo]' para adicionar nova entidade por tipo;
Digite 'search [id ou nome]' para buscar entidade por id ou nome;
Digite 'import [nome do arquivo]' para importar entidades ao banco de dados a partir de um arquivo .txt;
Digite 'config' para definir preferencias;
Digite 'help [comando]' para obter ajuda; 
Digite 'exit' para finalizar o programa.''')
    n=ask_input()
    if n[0] in cmds.keys():
        resp=cmds[n[0]](n)
        if resp!=0:
            print(erros[resp])
            temp=ask_input()
    else:
        print("Nao foi possivel identificar um comando, por favor digite Enter e tente novamente...")
        temp=ask_input()

while True: const_menu()