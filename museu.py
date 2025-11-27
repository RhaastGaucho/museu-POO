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
        self.init_db()

    def get_conexao(self):
        return sqlite3.connect('museu.db')
    
    def iniBD(self):
        
        conn = self.get_conexao(self.nome_bd)
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
            tabelaIns = "Obras"
        elif item is Artefatos:
            tabelaIns = "Artefatos"
        else:
            cursor.execute(
                "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data, descricao, setor, localidade, exposicao, nome, custo)
            )

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
        
        objeto = int(input(
            "Qual tipo de objeto você deseja inserir?\n\n"
            "[1] - Item (não classificado)\n" 
            "[2] - Obra de Arte\n" 
            "[3] - Artefato Histórico\n"
            "\n➤ Sua escolha: "
        ))

        if objeto == 1:
            print("\n" + "─"*70)
            print("CADASTRO DE ITEM NÃO CLASSIFICADO".center(70))
            print("─"*70 + "\n")

            data = input("Data de aquisição [Ex: 12/02/2002]: ")
            descricao = input("Descrição (o que é): ")
            setor = 'Análise'
            localidade = input("Localidade (onde o item foi encontrado): ")
            exposicao = False
            nome = ''
            custo = 0

            cursor.execute(
                "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data, descricao, setor, localidade, exposicao, nome, custo)
            )

            idFK = cursor.lastrowid

            conn.commit()
            
            item = Item(data, descricao, setor, idFK, localidade, exposicao, nome, custo)

            itens.append(item)

            print("\nItem cadastrado com sucesso! Enviado para o setor de Análise.\n")

        elif objeto == 2:
            print("\n" + "─"*70)
            print("CADASTRO DE OBRA DE ARTE".center(70))
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
                custo = 0.0

            # Insere na tabela Item
            cursor.execute(
                "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data, descricao, setor, localidade, exposicao, nome, custo)
            )

            # Pega o ID do item recém-inserido
            idFK = cursor.lastrowid

            conn.commit()

            # Agora insere os dados específicos da Obra
            autor = input("Autor da obra: ")
            movimentoArtistico = input("Movimento Artístico [Ex: Barroco, Renascimento]: ")
            restaurado = bool(int(input("A obra foi restaurada? (1 - Sim, 0 - Não): ")))
            if restaurado == 1:    
                dataRestauracao = input("Data da restauração [Ex: 12/03/2004]: ")
            else:
                dataRestauracao = ''

            cursor.execute(
                "INSERT INTO Obras (item_id, movimentoArtistico, restaurado, dataRestauracao, autor) VALUES (?,?,?,?,?)",
                (idFK, movimentoArtistico, restaurado, dataRestauracao, autor)
            )

            conn.commit()

            obra = Obras(data, descricao, setor, idFK, exposicao, nome, custo)
            
            print("\nObra de arte cadastrada com sucesso!\n")

        else:
            print("\n" + "─"*70)
            print("CADASTRO DE ARTEFATO HISTÓRICO".center(70))
            print("─"*70 + "\n")

            data = input("Data de aquisição [Ex: 12/02/2002]: ")
            descricao = input("Descrição: ")
            setor = input("Setor: ")
            localidade = input("Localidade (onde foi encontrado): ")
            exposicao = bool(int(input("Está em exposição? (1 - Sim, 0 - Não): ")))
            nome = input("Nome do artefato: ")
            if exposicao == 1:
                custo = input("Custo de exposição por mês: ")
            else:
                custo = 0.0

            # Insere na tabela Item
            cursor.execute(
                "INSERT INTO Item (data, descricao, setor, localidade, exposicao, nome, custoMes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data, descricao, setor, localidade, exposicao, nome, custo)
            )

            # Pega o ID do item recém-inserido
            idFK = cursor.lastrowid

            conn.commit()

            # Agora insere os dados específicos do Artefato
            epoca = input("Época [Ex: Pré-Histórico, Medieval]: ")
            fossil = bool(int(input("É um fóssil? (1 - Sim, 0 - Não): ")))
            mineral = bool(int(input("É um mineral? (1 - Sim, 0 - Não): ")))
            origemHumana = bool(int(input("Tem origem humana? (1 - Sim, 0 - Não): ")))

            cursor.execute(
                "INSERT INTO Artefatos (item_id, epoca, fossil, mineral, origemHumana) VALUES (?,?,?,?,?)",
                (idFK, epoca, fossil, mineral, origemHumana)
            )

            conn.commit()
            
            print("\nArtefato histórico cadastrado com sucesso!\n")

        print(f'ID do objeto adicionado: {idFK}')

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

            consulta = f"SELECT * FROM Item WHERE {campo} LIKE ?"
            cursor.execute(consulta, ('%' + valor + '%',)) 
            resultado = cursor.fetchall()

            if resultado:
                print("\nResultados encontrados:")
                for linha in resultado:
                    print(f"\nID: {linha[0]}")
                    print(f"Nome: {linha[1]}")
                    print(f"Data: {linha[2]}")
                    print(f"Descrição: {linha[3]}")
                    print(f"Setor: {linha[4]}")
                    print(f"Localidade: {linha[5]}")
                    print(f"Em exposição: {'Sim' if linha[6] else 'Não'}")
                    print(f"Custo mensal: {linha[7]}")
            else:
                print("\nNenhum resultado encontrado")
            
            input("\nPressione ENTER para continuar...")
        
        if consultabd == 2:
            print("\n" + "─"*70)
            print("CONSULTA DE OBRA".center(70))
            print("─"*70 + "\n")
            
            campo = input("Digite o campo para consulta (ex: nome, autor, movimentoArtistico): ")
            valor = input(f"Digite o valor para buscar em '{campo}': ")

            # JOIN entre Item e Obras
            consulta = f"""
            SELECT Item.id, Item.nome, Item.data, Item.descricao, Item.setor, 
                   Item.localidade, Item.exposicao, Item.custoMes,
                   Obras.autor, Obras.movimentoArtistico, Obras.restaurado, Obras.dataRestauracao
            FROM Item
            INNER JOIN Obras ON Item.id = Obras.item_id
            WHERE {campo} LIKE ?
            """
            cursor.execute(consulta, ('%' + valor + '%',))
            resultado = cursor.fetchall()

            if resultado:
                print("\nResultados encontrados:")
                for linha in resultado:
                    print(f"\nID: {linha[0]}")
                    print(f"Nome: {linha[1]}")
                    print(f"Data: {linha[2]}")
                    print(f"Descrição: {linha[3]}")
                    print(f"Setor: {linha[4]}")
                    print(f"Localidade: {linha[5]}")
                    print(f"Em exposição: {'Sim' if linha[6] else 'Não'}")
                    print(f"Custo mensal: {linha[7]}")
                    print(f"Autor: {linha[8]}")
                    print(f"Movimento Artístico: {linha[9]}")
                    print(f"Restaurado: {'Sim' if linha[10] else 'Não'}")
                    print(f"Data Restauração: {linha[11]}")
                    print("─"*70)
            else:
                print("\nNenhum resultado encontrado")
            
            input("\nPressione ENTER para continuar...")
        
        if consultabd == 3:
            print("\n" + "─"*70)
            print("CONSULTA DE ARTEFATO".center(70))
            print("─"*70 + "\n")
            
            campo = input("Digite o campo para consulta (ex: nome, epoca, localidade): ")
            valor = input(f"Digite o valor para buscar em '{campo}': ")

            # JOIN entre Item e Artefatos
            consulta = f"""
            SELECT Item.id, Item.nome, Item.data, Item.descricao, Item.setor, 
                   Item.localidade, Item.exposicao, Item.custoMes,
                   Artefatos.epoca, Artefatos.fossil, Artefatos.mineral, Artefatos.origemHumana
            FROM Item
            INNER JOIN Artefatos ON Item.id = Artefatos.item_id
            WHERE {campo} LIKE ?
            """
            cursor.execute(consulta, ('%' + valor + '%',))
            resultado = cursor.fetchall()

            if resultado:
                print("\nResultados encontrados:")
                for linha in resultado:
                    print(f"\nID: {linha[0]}")
                    print(f"Nome: {linha[1]}")
                    print(f"Data: {linha[2]}")
                    print(f"Descrição: {linha[3]}")
                    print(f"Setor: {linha[4]}")
                    print(f"Localidade: {linha[5]}")
                    print(f"Em exposição: {'Sim' if linha[6] else 'Não'}")
                    print(f"Custo mensal: {linha[7]}")
                    print(f"Época: {linha[8]}")
                    print(f"Fóssil: {'Sim' if linha[9] else 'Não'}")
                    print(f"Mineral: {'Sim' if linha[10] else 'Não'}")
                    print(f"Origem Humana: {'Sim' if linha[11] else 'Não'}")
                    print("─"*70)
            else:
                print("\nNenhum resultado encontrado")
            
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

            cursor.execute(f"UPDATE {tabelaAlt} SET {coluna} = '{novoValor}' WHERE {idTable} = {idAlt}")
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

                cursor.execute(f"UPDATE {tabelaAlt} SET data = '{data}', descricao = '{descricao}', localidade = '{localidade}' WHERE {idTable} = {idAlt}")
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

                cursor.execute(
                    f"UPDATE Item SET data = ?, descricao = ?, setor = ?, localidade = ?, exposicao = ?, nome = ?, custoMes = ? WHERE id = ?",
                    (data, descricao, setor, localidade, exposicao, nome, custo, idAlt)
                )
                
                autor = input("Autor da obra: ")
                movimentoArtistico = input("Movimento Artístico [Ex: Barroco, Renascimento]: ")
                restaurado = bool(int(input("A obra foi restaurada? (1 - Sim, 0 - Não): ")))
                if restaurado == 1:    
                    dataRestauracao = input("Data da restauração [Ex: 12/03/2004]: ")
                else:
                    dataRestauracao = ''

                cursor.execute(
                    f"UPDATE Obras SET movimentoArtistico = ?, restaurado = ?, dataRestauracao = ?, autor = ? WHERE item_id = ?",
                    (movimentoArtistico, restaurado, dataRestauracao, autor, idAlt)
                )
                
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

                cursor.execute(
                    f"UPDATE Item SET data = ?, descricao = ?, setor = ?, localidade = ?, exposicao = ?, nome = ?, custoMes = ? WHERE id = ?",
                    (data, descricao, setor, localidade, exposicao, nome, custo, idAlt)
                )
                
                epoca = input("Época [Ex: Pré-Histórico, Medieval]: ")
                fossil = bool(int(input("É um fóssil? (1 - Sim, 0 - Não): ")))
                mineral = bool(int(input("É um mineral? (1 - Sim, 0 - Não): ")))
                origemHumana = bool(int(input("Tem origem humana? (1 - Sim, 0 - Não): ")))

                cursor.execute(
                    f"UPDATE Artefatos SET epoca = ?, fossil = ?, mineral = ?, origemHumana = ? WHERE item_id = ?",
                    (epoca, fossil, mineral, origemHumana, idAlt)
                )
                
                conn.commit()
                print("\nArtefato atualizado com sucesso!\n")
        
        input("\nPressione ENTER para continuar...")
    
    if operacao == 4:
        print("\n" + "─"*70)
        print("EXCLUSÃO DE OBJETOS NO BANCO DO MUSEU".center(70))
        print("─"*70 + "\n")
        
        idDel = input("informe o ID do objeto que desejas excluir: ")

        cursor.execute(f"DELETE FROM Item WHERE id = {idDel}")
        conn.commit()
        
        print("\nObjeto excluido com sucesso!\n")
        
        input("\nPressione ENTER para continuar...")

conn.close()