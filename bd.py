import sqlite3
tipagem_id={
    "responsaveis":"rid",
    "setores":"sid",
    "ativos":"aid",
    "vulnerabilidades":"vid"
}
tipagem_nome={
    "responsaveis":"rnome",
    "setores":"snome",
    "ativos":"anome",
    "vulnerabilidades":"vnome"
}

class Database:
    def conectar(self): #Opens connection to database
        return sqlite3.connect(self.nome_banco)
    def criar_tabelas(self): #Creates tables if inexistent
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS responsaveis (
    rid INTEGER PRIMARY KEY AUTOINCREMENT,
    rnome TEXT NOT NULL
);""")
        cursor.execute("""                
CREATE TABLE IF NOT EXISTS setores (
    sid INTEGER PRIMARY KEY AUTOINCREMENT,
    snome TEXT NOT NULL
);""")
        cursor.execute("""      
CREATE TABLE IF NOT EXISTS ativos (
    aid INTEGER PRIMARY KEY AUTOINCREMENT,
    anome TEXT NOT NULL,
    setor INTEGER,
    categoria INTEGER,
    responsavel INTEGER,
    FOREIGN KEY(setor) REFERENCES setores(sid)
        ON DELETE CASCADE,
    FOREIGN KEY(responsavel) REFERENCES responsaveis(rid)
        ON DELETE CASCADE
);""")
        cursor.execute("""
CREATE TABLE IF NOT EXISTS vulnerabilidades (
    vid INTEGER PRIMARY KEY AUTOINCREMENT,
    vnome TEXT NOT NULL,
    severidade INTEGER,
    ativo INTEGER NOT NULL,
    vstatus TEXT DEFAULT 'Em Aberto.',
    descricao TEXT DEFAULT 'Sem descricao.',
    FOREIGN KEY(ativo) REFERENCES ativos(aid)
        ON DELETE CASCADE
);""")
        conexao.commit()
        conexao.close()
    def __init__(self, n): #Defines DB name property
        self.nome_banco = n
        self.criar_tabelas()
    def add_ativo(self, nom, categ, setor, respons): #Adds new entries to ativos table
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("""INSERT INTO ativos (anome, setor, categoria, responsavel) VALUES (?, ?, ?, ?)""", (nom, setor, categ, respons,))
        conexao.commit()
        lastid=cursor.lastrowid
        conexao.close()
        return lastid
    def add_setor(self, nom): #Adds new entries to setores table
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO setores (snome) VALUES (?)",(nom,))
        conexao.commit()
        lastid=cursor.lastrowid
        conexao.close()
        return lastid
    def add_resp(self, nom): #Adds new entries to responsaveis table
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO responsaveis (rnome) VALUES (?)",(nom,))
        conexao.commit()
        lastid=cursor.lastrowid
        conexao.close()
        return lastid
    def add_vul(self,nom,sev,atv,des,vstat): #Adds new entries to vulnerabilidades table
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO vulnerabilidades (vnome,severidade,ativo,descricao,vstatus) VALUES (?,?,?,?,?)",(nom,sev,atv,des,vstat,))
        conexao.commit()
        lastid=cursor.lastrowid
        conexao.close()
        return lastid
    def deletar(self,tabela,id,deps): #Deletes an entry + dependencies from its table
        conexao = self.conectar()
        cursor = conexao.cursor()
        if len(deps)>0:
            for x in deps:
                cursor.execute(f"DELETE FROM {x[1]} WHERE {tipagem_id[x[1]]} = ?",(x[0],))
        cursor.execute(f"DELETE FROM {tabela} WHERE {tipagem_id[tabela]} = ?",(id,))
        conexao.commit()
        conexao.close()
    def busca_lista(self,tabela): #Returns a list from all entries in a table
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM {tabela}")
        r = cursor.fetchall()
        conexao.close()
        return r
    def busca_vuln(self,id): #Returns a list os all vulnerabilities linkted to an item
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM vulnerabilidades WHERE ativo = ?",(id,))
        r = cursor.fetchall()
        conexao.close()
        return r
    def busca_id(self,tabela,a): #Returns an entity based on ID and table
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM {tabela} WHERE {tipagem_id[tabela]} = ?", (a,))
        r = cursor.fetchone()
        conexao.close()
        return r
    def cont_dep(self,tabela,id): #Returns a list of entities linked to another based on ID and table
        conexao = self.conectar()
        cursor = conexao.cursor()
        g=[]
        if tabela=="ativos":
            cursor.execute(f"SELECT * FROM vulnerabilidades WHERE ativo = ?",(id,))
            deps = cursor.fetchall()
            for x in deps:
                gg=(x[0],"vulnerabilidades")
                g.append(gg)
        elif tabela=="setores":
            cursor.execute(f"SELECT * FROM ativos WHERE setor = ?",(id,))
            deps = cursor.fetchall()
            for x in deps:
                cursor.execute(f"SELECT * FROM vulnerabilidades WHERE ativo = ?",(x[0],))
                vdeps=cursor.fetchall()
                for y in vdeps:
                    ggg=(y[0],"vulnerabilidades")
                    g.append(ggg)
                gg=(x[0],"ativos")
                g.append(gg)
        elif tabela=="responsaveis":
            cursor.execute(f"SELECT * FROM ativos WHERE responsavel = ?",(id,))
            deps = cursor.fetchall()
            for x in deps:
                cursor.execute(f"SELECT * FROM vulnerabilidades WHERE ativo = ?",(x[0],))
                vdeps=cursor.fetchall()
                for y in vdeps:
                    ggg=(y[0],"vulnerabilidades")
                    g.append(ggg)
                gg=(x[0],"ativos")
                g.append(gg)
        conexao.close()
        return g
    def atualizar(self,tabela,id,comm,nov): #Updates data of an entity
        try:
            conexao = self.conectar()
            cursor = conexao.cursor()
            cursor.execute(f"UPDATE {tabela} {comm} WHERE {tipagem_id[tabela]} = ?",(nov,id,))
            conexao.commit()
            conexao.close()
            return 0
        except: return 1
    def busca_nome(self,tabela,termo,a): #Fetches entries by name
        conexao = self.conectar()
        cursor = conexao.cursor()
        if a==0:
            cursor.execute(f"SELECT * FROM {tabela} WHERE {tipagem_nome[tabela]} = ?",(termo,)) #Exact search
            r = cursor.fetchone()
            conexao.close()
            return r
        else:
            cursor.execute(f"SELECT * FROM {tabela} WHERE {tipagem_nome[tabela]} LIKE ?",(f"%{termo}%",)) #Like search
            r = cursor.fetchall()
            conexao.close()
            return r