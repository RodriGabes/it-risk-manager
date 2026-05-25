import itrm_helper
import os
import bd

def exitfunc(n): #funcao de saida
    exit()

def clrScreen():
    try: os.system("cls")
    except: os.system("clear")

def ask_input(s): # funcao para a entrada de linha
    temp=input(">")
    n=temp.split(s)
    return n

conf={
    "bdatual":"mydata.db",
    "numlista":5
}

categorias={
    1:"NOTEBOOOK",
    2:"SERVIDOR",
    3:"ROTEADOR",
    4:"SOFTWARE LICENCIADO",
    5:"APLICACAO WEB",
    6:"BANCO DE DADOS",
    8:"IMPRESSORA DE REDE",
    9:"ESTACAO DE TRABALHO"
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
        u=ask_input(" ")
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
    return -1

def helper(n):
    try:
        if n[1] in list(itrm_helper.d.keys()):
                clrScreen()
                print(itrm_helper.d[n[1]])
                return 0
        else: return 2
    except: return 1

def add_to_bd(n):
    try:
        if n[1]=="a":
            clrScreen()
            print("""============
CADASTRAR ATIVO
============
-> Para cancelar o cadastro e voltar para o menu, digite 'exit'
-> Para continuar, digite em um unica linha, separado por ':', nesta ordem:
[NOME OU HOSTNAME]:[ID DO SETOR]:[ID DO RESPONSAVEL]""")
            u=ask_input(":")
            if u[0]=="exit": return 0
            try:
                hostnome=u[0]
                sid=int(u[1])
                rid=int(u[2])
                print("""
Por favor, digite o numero correspondente a categoria do ativo:
============
[1] NOTEBOOOK
[2] SERVIDOR
[3] ROTEADOR
[4] SOFTWARE LICENCIADO
[5] APLICACAO WEB
[6] BANCO DE DADOS
[8] IMPRESSORA DE REDE
[9] ESTACAO DE TRABALHO
============""")
                categ=int(ask_input(" "))
                bdados.add_ativo(hostnome,categ,sid,rid)
            except: return 1
            pass
        elif n[1]=="v":
            pass
        elif n[1]=="r":
            pass
        elif n[1]=="s":
            pass
        else: return 3
    except (ValueError,TypeError,OverflowError): return 4
    except (IndexError): return 1
    except: return 1

cmds={
    "add":add_to_bd,
    "search":2,
    "config":config,
    "help":helper,
    "exit":exitfunc
}

erros={
    1:"""O comando nao foi digitado corretamente ou faltam argumentos...
Use o comando 'help [comando] para verificar a sintaxe correta...""",
    2:"O comando que esta tentando verificar nao existe...",
    3:"A flag digitada nao e valida! As flags possiveis sao [r,v,s,a]...",
    4:"O ID digitado nao corresponde a um numero inteiro ou e invalido...",
    5:"a"
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
Digite 'config' para definir preferencias;
Digite 'help [comando]' para obter ajuda; 
Digite 'exit' para finalizar o programa.''')
    n=ask_input(" ")
    if n[0] in cmds.keys():
        resp=cmds[n[0]](n)
        if resp>-1:
            if resp>0:
                print(erros[resp])
            print("Digite [ENTER] para continuar...")
            temp=ask_input(" ")
    else:
        print("Nao foi possivel identificar um comando, por favor digite [ENTER] e tente novamente...")
        temp=ask_input(" ")


bdados=bd.Database(conf['bdatual'])
while True: const_menu()