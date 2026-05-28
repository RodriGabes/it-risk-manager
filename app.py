import itrm_helper
import os
import bd
import time

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
tipo_status={
    0:"CORRIGIDO",
    1:"EM ABERTO",
    2:"EM TRATAMENTO",
    3:"RISCO ACEITO"
}
tipo_severidade={
    0:"SEGURO",
    1:"POUCO IMPORTANTE",
    2:"IMPORTANTE",
    3:"MUITO IMPORTANTE",
    4:"CRITICO"
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
                categ=int(ask_input(" ")[0])
                novo_aid=bdados.add_ativo(hostnome,categ,sid,rid)
                print(f"-> NOVO ATIVO [{hostnome}] COM ID [{novo_aid}] CADASTRADO COM SUCESSO!")
            except: return 1
        elif n[1]=="v":
            clrScreen()
            print("""============
CADASTRAR VULNERABILIDADE
============
-> Para cancelar o cadastro e voltar para o menu, digite 'exit'
-> Para continuar, digite em um unica linha, separado por ':', nesta ordem:
[NOME DA VULNERABILIDADE]:[ID DO ATIVO]:[DESCRICAO]""")
            u=ask_input(":")
            if u[0]=="exit": return 0
            try:
                vnome=u[0]
                aid=int(u[1])
                vdesc=u[2]
                clrScreen()
                print(f"""============
CLASSIFICACAO DE SEVERIDADE
============
[0] SEGURO
[1] POUCO IMPORTANTE
[2] IMPORTANTE
[3] MUITO IMPORTANTE
[4] CRITICO
============
Para continuar, digite o numero correspondente a SEVERIDADE da vulnerabilidade [{vnome}] do ativo [{aid}]""")
                sev=int(ask_input(" ")[0])
                clrScreen()
                print(f"""============
STATUS DA VULNERABILIDADE
============
[0] CORRIGIDO
[1] EM ABERTO
[2] EM TRATAMENTO
[3] RISCO ACEITO
============
Para continuar, digite o numero correspondente ao STATUS da vulnerabilidade [{vnome}] do ativo [{aid}]""")
                stat=int(ask_input(" ")[0])
                novo_vid=bdados.add_vul(vnome, sev, aid, vdesc, stat)
                print(f"-> NOVA VULNERABILIDADE [{vnome}] COM ID [{novo_vid}] CADASTRADA COM SUCESSO!")
            except: return 1
        elif n[1]=="r":
            clrScreen()
            print("""============
CADASTRAR RESPONSAVEL
============
-> Para cancelar o cadastro e voltar para o menu, digite 'exit'
-> Para continuar, digite em um unica linha o nome do responsavel:""")
            u=ask_input(":")
            if u[0]=="exit": return 0
            # adicionar: pesquisa nominal para recusa de abertura identica
            try:
                novo_rid=bdados.add_resp(u[0])
                print(f"-> NOVO RESPONSAVEL [{u[0]}] COM ID [{novo_rid}] CADASTRADO COM SUCESSO!")
            except: return 1
        elif n[1]=="s":
            clrScreen()
            print("""============
CADASTRAR SETOR
============
-> Para cancelar o cadastro e voltar para o menu, digite 'exit'
-> Para continuar, digite em um unica linha o nome do setor:""")
            u=ask_input(":")
            if u[0]=="exit": return 0
            # adicionar: pesquisa nominal na tabela de setores para recusa de abertura identica
            try:
                novo_sid=bdados.add_setor(u[0])
                print(f"-> NOVO SETOR [{u[0]}] COM ID [{novo_sid}] CADASTRADO COM SUCESSO!")
            except: return 1
        else: return 3
    except (ValueError,TypeError,OverflowError): return 4
    except (IndexError): return 1
    except: return 1
    return 0

flags={
    "v":"vulnerabilidades",
    "r":"responsaveis",
    "a":"ativos",
    "s":"setores"
}
mods_perm={
    "v":[1,2,3,4,5],
    "r":[1],
    "a":[1,6,7,8],
    "s":[1]
}
mods={
    "1a":"SET anome = ?",
    "1v":"SET vnome = ?",
    "1s":"SET snome = ?",
    "1r":"SET rnome = ?",
    "2v":"SET vstatus = ?",
    "3v":"SET severidade = ?",
    "4v":"SET ativo = ?",
    "5v":"SET descricao = ?",
    "6a":"SET responsavel = ?",
    "7a":"SET setor = ?",
    "8a":"SET categoria = ?"
}
def select(t,f,id):
    while True:
        clrScreen()
        vulns=[]
        if f=="a":
            sec=bdados.busca_id("setores",t[2])
            res=bdados.busca_id("responsaveis",t[4])
            vulns=bdados.busca_vuln(t[0])
            print(f"""-> [ATIV] ID=[{t[0]}] HOSTNOME=[{t[1]}] CATEGORIA=[{t[3]}:"{categorias[t[3]]}"]
    RESPONSAVEL=[{t[4]}:"{res[1]}"]
    SETOR=[{t[2]}:"{sec[1]}"]
    CONTAGEM DE VULNERABILIDADES={len(vulns)}""")
        elif f=="v":
            print(f"""-> [VULN] ID=[{t[0]}] NOME=[{t[1]}] SEVERIDADE=[{tipo_severidade[t[2]]}] ATIVO_ID=[{t[3]}] STATUS=[{tipo_status[int(t[4])]}]
   DESCRICAO=[{t[5]}]""")
        elif f=="r": print(f"-> [RESP] ID=[{t[0]}] NOME=[{t[1]}]")
        else: print(f"-> [SETR] ID=[{t[0]}] NOME=[{t[1]}]")
        print("""============
OPCOES
============
Digite 'exit' para voltar ao menu...
Digite 'del' para deletar esta entidade...
Digite 'mod' para modificar dados desta entidade...""")
        if f=="a": print("Digite 'vuln' para visualizar a lista de vulnerabilidades...")
        print("============")
        hh=ask_input(" ")
        if hh[0]=="exit":
            return -1
        elif hh[0]=="del":
            deps=bdados.cont_dep(flags[f],id)
            if len(deps)>0:
                print(f"""============
ATENCAO!
============
Esta entidade possui {len(deps)} dependencia(s). Ao deletar esta entidade, todas as suas dependencias seram deletadas tambem...
Gostaria de deletar mesmo assim? (s/n)""")
                resp=ask_input(" ")
                if resp[0]=="s" or resp[0]=="S":
                    try:
                        bdados.deletar(flags[f],id,deps)
                        print("Entidades deletada com sucesso!")
                        break
                    except: print("Nao foi possivel deletar esta entidade...")
                else: print("Operacao abortada...")
            else:
                try:
                    lvazia=[]
                    bdados.deletar(flags[f],id,lvazia)
                    print("Entidade deletada com sucesso!")
                    break
                except: print("Nao foi possivel deletar esta entidade...")
        elif hh[0]=="vuln" and f=="a":
            clrScreen()
            pags=1
            cont=0
            elemns=len(vulns)
            pags+=elemns//conf["numlista"]
            if elemns==conf["numlista"]: pags-=1
            for w in range(pags):
                print(f"""============
LISTA DE VULNERABILIDADES
Exibindo pagina {w+1} de {pags}:
============""")
                for ww in range(conf["numlista"]):
                    try:
                        print(f"""-> [{vulns[cont][0]}]:"{vulns[cont][1]}" STATUS: {tipo_status[int(vulns[cont][4])]}, SEVERIDADE: {tipo_severidade[vulns[cont][2]]}
   DESCRICAO: {vulns[cont][5]}
------------""")
                        cont+=1
                    except: break
                print("Digite [ENTER] para prosseguir a proxima pagina ou 'exit' para sair...")
                resp1=ask_input(" ")
                if resp1=="exit":break
        elif hh[0]=="mod":
            clrScreen()
            print(f"""=============
MODIFICAR UMA ENTIDADE
============
[1] Para modificar o NOME de [{t[1]}]...""")
            if f=="v":
                print("""[2] Para modificar o STATUS da [VULNERABILIDADE]...
[3] Para modificar a SEVERIDADE da [VULNERABILIDADE]...
[4] Para modificar o ATIVO da [VULNERABILIDADE]...
[5] Para modificar a DESCRICAO da [VULNERABILIDADE]...""")
            elif f=="a":
                print("""[6] Para modificar o RESPONSAVEL do [ATIVO]...
[7] Para modificar o SETOR do [ATIVO]...
[8] Para modificar a CATEGORIA do [ATIVO]...""")
            while True:
                k=ask_input(" ")
                if k[0]=="exit": break
                if int(k[0]) in mods_perm[f]:
                    nov=""
                    if k[0]=="2":
                        print("""============
STATUS DA VULNERABILIDADE
============
[0] CORRIGIDO
[1] EM ABERTO
[2] EM TRATAMENTO
[3] RISCO ACEITO
============""")
                        while True:
                            nvvul=ask_input(" ")
                            if nvvul[0]=="exit": break
                            try:
                                if int(nvvul[0]) in [0,1,2,3]:
                                    nov=nvvul[0]
                                    break
                                else: print("Por favor, digite um opcao valida...")
                            except: print("Por favor, digite um opcao valida...")
                    elif k[0]=="3":
                        print("""============
CLASSIFICACAO DE SEVERIDADE
============
[0] SEGURO
[1] POUCO IMPORTANTE
[2] IMPORTANTE
[3] MUITO IMPORTANTE
[4] CRITICO
============""")
                        while True:
                            nvsev=ask_input(" ")
                            if nvsev[0]=="exit":break
                            try:
                                if int(nvsev[0]) in [0,1,2,3,4]:
                                    nov=int(nvsev[0])
                                    break
                                else: print("Por favor, digite um opcao valida...")
                            except: print("Por favor, digite um opcao valida...")
                    else:
                        print("Por favor, digite o novo valor desejado:")
                        k0=ask_input(":")
                        if int(k[0]) in [4,6,7,8]:
                            try:
                                nov=int(k0[0])
                            except: print("-> O novo valor para este ID deve ser um inteiro!")
                        else: nov=k0[0]
                    modkey=k[0]+f
                    resp=bdados.atualizar(flags[f],id,mods[modkey],nov)
                    if resp==1: print("-> Nao foi possivel atualizar os dados...")
                    else: print("""-> Dados atualizados com sucesso!
============
Digite 'exit' para voltar ao menu...
Digite 'del' para deletar esta entidade...
Digite 'mod' para modificar dados desta entidade...
============""")
                    break
                else:
                    print("-> Por favor, digite uma opcao valida...")
                    time.sleep(3)
        else: 
            print("-> Por favor, digite um comando valido...")
            time.sleep(3)
    return 0

def search_bd(n):
    normal=0
    try:
        flag=n[1]
        tp=n[2]
        retorno=[]
        if tp=="id": # busca por id > select / concluido
            termo=int(n[3])
            r=bdados.busca_id(flags[flag],termo)
            if r==None:
                print(f"Nenhuma entidade com ID = [{termo}] encontrada na tabela [{flags[flag]}]!")
            else:
                ii=select(r,flag,r[0])
                if ii==-1: normal=-1
        elif tp=="nm": # busca textual / concluido
            termo=n[3]
            retorno=bdados.busca_nome(flags[flag],termo)
        elif tp=="ls": # fetching da lista / concluido
            retorno=bdados.busca_lista(flags[flag])
        else: return 1
        if len(retorno)!=0: #exibicao da lista + select / concluido
            elemns=len(retorno)
            pags=1
            cont=0
            pags+=elemns//conf["numlista"]
            if elemns==conf["numlista"]: pags-=1
            for w in range(pags):
                print(f"""============
LISTAGEM
Exibindo pagina {w+1} de {pags}:
============""")
                for ww in range(conf["numlista"]):
                    try:
                        print(f"""-> [{retorno[cont][0]}]:'{retorno[cont][1]}'""")
                        cont+=1
                    except: break
                print("------------")
                print("""Digite [ENTER] para prosseguir a proxima pagina...
Digite o ID de uma entidade para ver detalhes...
Digite 'exit' para sair...""")
                resp1=ask_input(" ")
                if resp1[0]=="exit":
                    normal=-1
                    break
                try:
                    pid=int(resp1[0])
                    t=bdados.busca_id(flags[flag],pid)
                    if t==None:
                        print("Nao ha nenhuma entidade nesta tabela com o ID digitado...")
                        break
                    else: 
                        ii=select(t,flag,pid)
                        if ii==-1:normal=-1
                    break
                except: pass  
    except: return 1
    return normal

cmds={
    "add":add_to_bd,
    "search":search_bd,
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
Digite 'search [tipo] [id/nm/ls]' para buscar entidades de um tipo por id ou nome;
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

bdados=bd.Database(conf['bdatual']) ## como reiniciaizar outro bdados?
while True: const_menu()