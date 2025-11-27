import sqlite3
conn = sqlite3.connect('museu.db')
cursor = conn.cursor()

itens = []

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

class BancoDeDados():
    def __init__(self, nome_bd='museu.db'):
        self.nome_bd = nome_bd
        self.iniBD()

    def get_conexao(self):
        return sqlite3.connect('museu.db')
    
    def iniBD(self):
        
        conn = self.get_conexao()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            descricao VARCHAR(255) NOT NULL,
            setor VARCHAR(255) NOT NULL,
            localidade VARCHAR(255) NOT NULL,
            exposicao BOOLEAN,
            nome VARCHAR(255),
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
            FOREIGN KEY(item_id) REFERENCES Item(id) ON DELETE CASCADE
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Artefatos (
            item_id INTEGER PRIMARY KEY,
            epoca VARCHAR(255),
            fossil BOOLEAN,
            mineral BOOLEAN,
            origemHumana BOOLEAN,
            FOREIGN KEY(item_id) REFERENCES Item(id) ON DELETE CASCADE
        );
        ''')

        conn.commit()
    def inserir(self, item):
        if item is Obras:
            cursor.execute(
                "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item.data, item.descricao, item.setor, item.localidade, item.exposicao, item.nome, item.custoMes)
            )
            
            idFK = cursor.lastrowid
            
            cursor.execute(
                "INSERT INTO Obras (item_id, movimentoArtistico, restaurado, dataRestauracao, autor) VALUES (?,?,?,?,?)",
                (idFK, item.movimentoArtistico, item.restaurado, item.dataRestauracao, item.autor)
            )
        elif item is Artefatos:
            cursor.execute(
                "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item.data, item.descricao, item.setor, item.localidade, item.exposicao, item.nome, item.custoMes)
            )
            
            idFK = cursor.lastrowid
            
            cursor.execute(
                "INSERT INTO Artefatos (item_id, epoca, fossil, mineral, origemHumana) VALUES (?,?,?,?,?)",
                (idFK, epoca, fossil, mineral, origemHumana)
            )
        else:
            cursor.execute(
                "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item.data, item.descricao, item.setor, item.localidade, item.exposicao, item.nome, item.custoMes)
            )
    def consultar(self, tabela, campo, valor):
        conn = self.get_conexao(self.nome_bd)
        cursor = conn.cursor()
        consulta = f"SELECT * FROM {tabela} WHERE {campo} = ?"
        cursor.execute(consulta, (valor,))
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    def update(self, tabela, id, coluna, novo_valor):
        conn = self.get_conexao(self.nome_bd)
        cursor = conn.cursor()
        consulta = f"UPDATE {tabela} SET {coluna} = ? WHERE id = ?"
        cursor.execute(consulta, (novo_valor, id))
        conn.commit()
        conn.close()
    def deletar(self, tabela, id):
        conn = self.get_conexao(self.nome_bd)
        cursor = conn.cursor()
        consulta = f"DELETE FROM {tabela} WHERE id = ?"
        cursor.execute(consulta, (id,))
        conn.commit()
        conn.close()

bd = BancoDeDados()

bd.iniBD()

print("\n" + "="*70)
print("BEM-VINDO AO SISTEMA DE GERENCIAMENTO DO MUSEU".center(70))
print("="*70 + "\n")

while True:
    print("\n" + "─"*70)
    print("MENU DE OPERAÇÕES".center(70))
    print("─"*70 + "\n")

    operacao = int(input(
        "Escolha uma operação digitando o número correspondente:\n\n"
        "[1] - Inserir novos itens no acervo do museu\n"
        "[2] - Consultar itens cadastrados no banco de dados\n"
        "[3] - Alterar informações de itens existentes\n"
        "[4] - Excluir itens do banco de dados\n"
        "[5] - Sair do sistema\n"
        "\n➤ Sua escolha: "
    ))

    if operacao == 5:
        print("\n" + "─"*70)
        print("Encerrando o sistema... Até logo!".center(70))
        print("─"*70 + "\n")
        break

    if operacao == 1:
        print("\n" + "─"*70)
        print("INSERÇÃO DE NOVOS ITENS".center(70))
        print("─"*70 + "\n")
        
        ajuda = int(input(
            "Você pode inserir um Item, uma Obra ou um Artefato.\n"
            "Você deseja uma explicação para saber qual escolher?\n\n"
            "  [1] - Não preciso de ajuda, já sei como o sistema funciona\n"
            "  [2] - Preciso de ajuda, não sei o que vou inserir\n"
            "\n➤ Sua escolha: "
        ))
        
        if ajuda == 2:
            print("\n" + "="*70)
            print("GUIA DE CLASSIFICAÇÃO - ENTENDA A DIFERENÇA".center(70))
            print("="*70 + "\n")
            
            print("ITEM:")
            print("   Insira como 'Item' quando a peça ainda não foi classificada por um")
            print("   museólogo especializado. Esses objetos são enviados ao setor de")
            print("   Análise, onde profissionais qualificados irão determinar se é uma")
            print("   Obra de Arte ou um Artefato histórico.\n")
            
            print("OBRA:")
            print("   Obras são criações artísticas produzidas intencionalmente por seres")
            print("   humanos com propósito estético ou cultural. Incluem pinturas,")
            print("   esculturas, tapeçarias, cerâmicas decorativas, entre outras")
            print("   manifestações artísticas.\n")
            
            print("ARTEFATO:")
            print("   Artefatos são objetos de valor histórico, arqueológico ou científico.")
            print("   Podem ser de origem humana (ferramentas antigas, inscrições rupestres)")
            print("   ou natural (fósseis, minerais, rochas com relevância científica).")
            print("   São peças que documentam a história natural ou cultural.\n")
            
            print("="*70)
            input("Pressione ENTER para continuar...")
            print("\n")
        
        criarTipo = int(input("Você deseja criar um Item, Obra ou Artefato? \n" 
            "[1] - Item\n"
            "[2] - Obra\n" 
            "[3] - Artefato\n"
            "\n➤ Sua escolha: "))
        
        if criarTipo == 1:
            print("\n" + "─"*70)
            print("CRIAÇÃO DE ITEM".center(70))
            print("─"*70 + "\n")
            
            data = input("Data de aquisição [Ex: 12/02/2002]: ")
            descricao = input("Descrição (o que é): ")
            setor = input("Setor: ")
            localidade = input("Localidade (onde o item foi encontrado): ")
            exposicao = bool(int(input("Está em exposição? (1 - Sim, 0 - Não): ")))
            nome = input("Nome do item: ")
            if exposicao == 1:    
                custo = input("Custo de exposição por mês: ")
            else:
                custo = 0

            novoItem = Item(data, descricao, setor, None, localidade, exposicao, nome, custo)
            bd.inserir(novoItem)
            conn.commit()

        elif criarTipo == 2:
            print("\n" + "─"*70)
            print("CRIAÇÃO DE OBRA".center(70))
            print("─"*70 + "\n")

            data = input("Data de aquisição [Ex: 12/02/2002]: ")
            descricao = input("Descrição (ex: óleo sobre tela): ")
            setor = input("Setor: ")
            localidade = input("Localidade (onde foi encontrado): ")
            exposicao = bool(int(input("Está em exposição? (1 - Sim, 0 - Não): ")))
            nome = input("Nome da obra: ")
            if exposicao == 1:    
                custo = input("Custo de exposição por mês: ")
            else:
                custo = 0

            autor = input("Autor da obra: ")
            movimentoArtistico = input("Movimento Artístico [Ex: Barroco, Renascimento]: ")
            restaurado = bool(int(input("A obra foi restaurada? (1 - Sim, 0 - Não): ")))
            if restaurado == 1:    
                dataRestauracao = input("Data da restauração [Ex: 12/03/2004]: ")
            else:
                dataRestauracao = ''

            novaObra = Obras(data, descricao, setor, None, localidade, exposicao, nome, custo, movimentoArtistico, restaurado, dataRestauracao, autor)
            bd.inserir(novaObra)
            conn.commit()
        elif criarTipo == 3:
            print("\n" + "─"*70)
            print("CRIAÇÃO DE ARTEFATO".center(70))
            print("─"*70 + "\n")

            data = input("Data de aquisição [Ex: 12/02/2002]: ")
            descricao = input("Descrição: ")
            setor = input("Setor: ")
            localidade = input("Localidade (onde foi encontrado): ")
            exposicao = bool(int(input("Está em exposição? (1 - Sim, 0 - Não): ")))
            nome = input("Nome do artefato: ")
            custo = input("Custo de exposição por mês: ")

            epoca = input("Época [Ex: Pré-Histórico, Medieval]: ")
            fossil = bool(int(input("É um fóssil? (1 - Sim, 0 - Não): ")))
            mineral = bool(int(input("É um mineral? (1 - Sim, 0 - Não): ")))
            origemHumana = bool(int(input("Tem origem humana? (1 - Sim, 0 - Não): ")))

            novoArtefato = Artefatos(data, descricao, setor, None, localidade, exposicao, nome, custo, epoca, fossil, mineral, origemHumana)
            bd.inserir(novoArtefato)
            conn.commit()
        
        print("\nItem inserido com sucesso!\n")
            
        input("\nPressione ENTER para continuar...")
        
    if operacao == 2:
        print("\n" + "─"*70)
        print("CONSULTA DE OBJETOS NO BANCO DO MUSEU".center(70))
        print("─"*70 + "\n")

        consultabd = int(input("Você deseja consultar um Item, Obra ou Artefato? \n" 
            "[1] - Item\n"
            "[2] - Obra\n" 
            "[3] - Artefato\n"
            "\n➤ Sua escolha: "))
        if consultabd == 1:
            print("\n" + "─"*70)
            print("CONSULTA DE ITENS".center(70))
            print("─"*70 + "\n")
            
            campo = input("Digite o campo para consulta (ex: nome, setor, localidade): ")
            valor = input(f"Digite o valor para buscar em '{campo}': ")

            bd.consultar("Item", campo, valor)
            
            input("\nPressione ENTER para continuar...")
        
        if consultabd == 2:
            print("\n" + "─"*70)
            print("CONSULTA DE OBRA".center(70))
            print("─"*70 + "\n")
            
            campo = input("Digite o campo para consulta (ex: nome, autor, movimentoArtistico): ")
            valor = input(f"Digite o valor para buscar em '{campo}': ")

            bd.consultar("Obras", campo, valor)
              
            input("\nPressione ENTER para continuar...")
        
        if consultabd == 3:
            print("\n" + "─"*70)
            print("CONSULTA DE ARTEFATO".center(70))
            print("─"*70 + "\n")
            
            campo = input("Digite o campo para consulta (ex: nome, epoca, localidade): ")
            valor = input(f"Digite o valor para buscar em '{campo}': ")

            bd.consultar("Artefatos", campo, valor)  
            
            input("\nPressione ENTER para continuar...")

    if operacao == 3:
        print("\n" + "─"*70)
        print("ALTERAÇÃO DE OBJETOS NO BANCO DO MUSEU".center(70))
        print("─"*70 + "\n")
        
        alterarCelulaLinha = int(input("Você deseja alterar uma célula ou uma linha inteira? \n" 
        "[1] - Desejo alterar uma única célula \n" 
        "[2] - Desejo alterar uma linha inteira\n "
        "\n➤ Sua escolha: "))

        if alterarCelulaLinha == 1:
            print("\n" + "─"*70)
            print("ALTERAR CÉLULA DO BANCO DE DADOS DO MUSEU".center(70))
            print("─"*70 + "\n")

            alterarTable = int(input("Informe a tabela que deseja alterar: \n" 
            "[1] - Item \n" 
            "[2] - Obras\n" 
            "[3] - Artefatos\n"
            "\n➤ Sua escolha: "))

            if alterarTable == 1:
                tabelaAlt = "Item"
                idTable = "id"
            elif alterarTable == 2:
                tabelaAlt = "Obras"
                idTable = "item_id"
            elif alterarTable == 3:
                tabelaAlt = "Artefatos"
                idTable = "item_id"

            idAlt = input("Informe o ID do objeto: ")
            coluna = input("Informe a coluna que deseja alterar: ")
            novoValor = input("Informe o novo valor da célula: ")

            bd.update(tabelaAlt, idAlt, coluna, novoValor)
            conn.commit()

        elif alterarCelulaLinha == 2:
            print("\n" + "─"*70)
            print("ALTERAR LINHA DA TABELA ITEM".center(70))
            print("─"*70 + "\n")
            
            alterarTable = int(input("Informe a tabela que deseja alterar: \n" 
            "[1] - Item \n" 
            "[2] - Obras\n" 
            "[3] - Artefatos\n"
            "\n➤ Sua escolha: "))

            if alterarTable == 1:
                tabelaAlt = "Item"
                idTable = "id"
            elif alterarTable == 2:
                tabelaAlt = "Obras"
                idTable = "item_id"
            elif alterarTable == 3:
                tabelaAlt = "Artefatos"
                idTable = "item_id"

            idAlt = input("Informe o ID do objeto: ")

            if alterarTable == 1:
                data = input("Data de aquisição [Ex: 12/02/2002]: ")
                descricao = input("Descrição (o que é): ")
                localidade = input("Localidade (onde o item foi encontrado): ")

                bd.update("Item", idAlt, "data", data)
                bd.update("Item", idAlt, "descricao", descricao)
                bd.update("Item", idAlt, "localidade", localidade)
                
                conn.commit()
                print("\nItem atualizado com sucesso!\n")
                
            elif alterarTable == 2:
                print("\n" + "─"*70)
                print("ALTERAR LINHA DA TABELA OBJETOS".center(70))
                print("─"*70 + "\n")

                data = input("Data de aquisição [Ex: 12/02/2002]: ")
                descricao = input("Descrição (ex: óleo sobre tela): ")
                setor = input("Setor: ")
                localidade = input("Localidade (onde foi encontrado): ")
                exposicao = bool(int(input("Está em exposição? (1 - Sim, 0 - Não): ")))
                nome = input("Nome da obra: ")
                if exposicao == 1:    
                    custo = input("Custo de exposição por mês: ")
                else:
                    custo = 0
                autor = input("Autor da obra: ")
                movimentoArtistico = input("Movimento Artístico [Ex: Barroco, Renascimento]: ")
                restaurado = bool(int(input("A obra foi restaurada? (1 - Sim, 0 - Não): ")))
                if restaurado == 1:    
                    dataRestauracao = input("Data da restauração [Ex: 12/03/2004]: ")
                else:
                    dataRestauracao = ''
                bd.update("Item", idAlt, "data", data)
                bd.update("Item", idAlt, "descricao", descricao)
                bd.update("Item", idAlt, "localidade", localidade)
                bd.update("Item", idAlt, "setor", setor)
                bd.update("Item", idAlt, "exposicao", exposicao)
                bd.update("Item", idAlt, "nome", nome)
                bd.update("Item", idAlt, "custoMes", custo)
                bd.update("Obras", idAlt, "autor", autor)
                bd.update("Obras", idAlt, "movimentoArtistico", movimentoArtistico)
                bd.update("Obras", idAlt, "restaurado", restaurado)
                bd.update("Obras", idAlt, "dataRestauracao", dataRestauracao)
                
                conn.commit()
                print("\nObra atualizada com sucesso!\n")
                
            elif alterarTable == 3:
                print("\n" + "─"*70)
                print("ALTERAR LINHA DA TABELA ARTEFATOS".center(70))
                print("─"*70 + "\n")

                data = input("Data de aquisição [Ex: 12/02/2002]: ")
                descricao = input("Descrição: ")
                setor = input("Setor: ")
                localidade = input("Localidade (onde foi encontrado): ")
                exposicao = bool(int(input("Está em exposição? (1 - Sim, 0 - Não): ")))
                nome = input("Nome do artefato: ")
                custo = input("Custo de exposição por mês: ")
                epoca = input("Época [Ex: Pré-Histórico, Medieval]: ")
                fossil = bool(int(input("É um fóssil? (1 - Sim, 0 - Não): ")))
                mineral = bool(int(input("É um mineral? (1 - Sim, 0 - Não): ")))
                origemHumana = bool(int(input("Tem origem humana? (1 - Sim, 0 - Não): ")))

                bd.update("Item", idAlt, "data", data)
                bd.update("Item", idAlt, "descricao", descricao)
                bd.update("Item", idAlt, "localidade", localidade)
                bd.update("Item", idAlt, "setor", setor)
                bd.update("Item", idAlt, "exposicao", exposicao)
                bd.update("Item", idAlt, "nome", nome)
                bd.update("Item", idAlt, "custoMes", custo)
                bd.update("Artefatos", idAlt, "epoca", epoca)
                bd.update("Artefatos", idAlt, "fossil", fossil)
                bd.update("Artefatos", idAlt, "mineral", mineral)
                bd.update("Artefatos", idAlt, "origemHumana", origemHumana)
                
                conn.commit()
                print("\nArtefato atualizado com sucesso!\n")
        
        input("\nPressione ENTER para continuar...")
    
    if operacao == 4:
        print("\n" + "─"*70)
        print("EXCLUSÃO DE OBJETOS NO BANCO DO MUSEU".center(70))
        print("─"*70 + "\n")
        
        idDel = input("informe o ID do objeto que desejas excluir: ")

        bd.deletar("Item", idDel)
        conn.commit()
        
        print("\nObjeto excluido com sucesso!\n")
        
        input("\nPressione ENTER para continuar...")

conn.close()
