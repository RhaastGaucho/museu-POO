import sqlite3
conn = sqlite3.connect('meu_banco.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    setor VARCHAR(255) NOT NULL,
    localidade VARCHAR(255) NOT NULL,
    exposicao BOOLEAN,
    nome VARCHAR(255) NOT NULL,
    custoMes VARCHAR(255)
);
''')

conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Obras (
    item_id INTEGER PRIMARY KEY,
    movimentoArtistico VARCHAR(255),
    restaurado BOOLEAN,
    dataRestauracao DATE,
    autor VARCHAR(255),
    FOREIGN KEY(item_id) REFERENCES Item(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Artefatos (
    item_id INTEGER PRIMARY KEY,
    epoca VARCHAR(255),
    fossil BOOLEAN,
    mineral BOOLEAN,
    origemHumana BOOLEAN,
    FOREIGN KEY(item_id) REFERENCES Item(id)
);
''')

conn.commit()

class Item:
    def __init__(self, data, descricao, setor, id, localidade, exposicao, nome, custo):
        self.data = data
        self.descricao = descricao
        self.setor = setor
        self.id = id
        self.localidade = localidade
        self.exposicao = exposicao
        self.nome = nome
        self.custoMes = custo

    def setCustoExposicao(self, custo):
        self.custoMes = custo

class Obras(Item):
    def __init__(self,  data, descricao, setor, id, localidade, exposicao, nome, custo, movimentoArtistico, restaurado = False, dataRestauracao = None, autor = "Desconhecido"):
        super().__init__(data, descricao, setor, id, localidade, exposicao, nome, custo)
        self.autor = autor
        self.movimentoArtistico = movimentoArtistico
        self.restaurado = restaurado
        self.dataRestauracao = dataRestauracao

    def restaurarObra(self, custo, tipo, data):
        self.custo = custo
        self.tipo = tipo
        self.dataRestauracao = data
        self.restaurado = True

class Artefatos(Item):
    def __init__(self,  data, descricao, setor, id, localidade, exposicao, nome, custo, epoca, fossil, mineral, origemHumana):
        super().__init__(data, descricao, setor, id, localidade, exposicao, nome, custo)
        self.epoca = epoca
        self.fossil = fossil
        self.mineral = mineral
        self.origemHumana = origemHumana
        self.emprestado = False

    def reservaEstudo(self, pesquisador, instituicao):
        self.exposicao = False
        self.pesquisador = pesquisador
        self.instituicao = instituicao
        self.emprestado = True

a1 = Artefatos("2000", "Pedra", "Geologia", 9999, "Georgia", True, "Pedra", 9, "Contemporanea", False, True, False)
259
# cursor.execute(
#     "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
#     (a1.data, a1.descricao, a1.setor, a1.localidade, a1.exposicao, a1.nome, a1.custoMes)
# )

# cursor.execute(
#     "INSERT INTO Artefatos (item_id, epoca, fossil, mineral, origemHumana) VALUES (?,?,?,?,?)",
#     (1, a1.epoca, a1.fossil, a1.mineral, a1.origemHumana)
# )


cursor.execute('''
    SELECT *
    FROM Item
    JOIN Artefatos ON Item.id = Artefatos.item_id
''')

resultado = cursor.fetchall()

for linha_completa in resultado:
    print(linha_completa)

conn.commit()

print("Escreva os valores da linha: ")

data = input("Data: ")
descricao = input("Descricao: ")
setor = input("Setor: ")
localidade = input("Localidade: ")
exposicao = input("Está em exposição: ")
nome = input("Nome: ")
custo = input("Custo de expposição por mês: ")
epoca = input("Epoca: ")
fossil = input("Fóssil: ")
mineral = input("Mineral: ")
origemHumana = input("Origem humana: ")

cursor.execute(
    "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (data, descricao, setor, localidade, exposicao, nome, custo)
)

cursor.execute("SELECT id FROM Item")

idFK = cursor.lastrowid

conn.commit()

cursor.execute(
   "INSERT INTO Artefatos (item_id, epoca, fossil, mineral, origemHumana) VALUES (?,?,?,?,?)",
    (idFK, epoca, fossil, mineral, origemHumana)
)

conn.commit()

conn.close()
