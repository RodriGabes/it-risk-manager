import sqlite3

class Database:
    def conectar(self):
        return sqlite3.connect(self.nome_banco)

    def criar_tabelas(self):
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
    FOREIGN KEY(setor) REFERENCES setores(sid),
    FOREIGN KEY(responsavel) REFERENCES responsaveis(rid)
);""")
        cursor.execute("""
CREATE TABLE IF NOT EXISTS vulnerabilidades (
    vid INTEGER PRIMARY KEY AUTOINCREMENT,
    vnome TEXT NOT NULL,
    severidade INTEGER,
    ativo INTEGER NOT NULL,
    descricao TEXT DEFAULT 'Sem descricao.',
    FOREIGN KEY(ativo) REFERENCES ativos(aid)
        ON DELETE CASCADE
);""")

        conexao.commit()
        conexao.close()

    def __init__(self, n):
        self.nome_banco = n
        self.criar_tabelas()

    def add_ativo(self, nom, categ, setor, respons):
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO ativos (anome, setor, categoria, responsavel)
            VALUES (?, ?, ?, ?)
        """, (nom, setor, categ, respons))
        conexao.commit()
        lastid=cursor.lastrowid
        conexao.close()
        return lastid

    def listar_usuarios(self):
        conexao = self.conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM usuarios")

        usuarios = cursor.fetchall()

        conexao.close()

        return usuarios