import sqlite3
conn = sqlite3.connect('museu.db')
cursor = conn.cursor()

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

            conn.commit()
            
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
            custo = input("Custo de exposição por mês: ")

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
            dataRestauracao = input("Data da restauração [Ex: 12/03/2004]: ")

            cursor.execute(
                "INSERT INTO Obras (item_id, movimentoArtistico, restaurado, dataRestauracao, autor) VALUES (?,?,?,?,?)",
                (idFK, movimentoArtistico, restaurado, dataRestauracao, autor)
            )

            conn.commit()
            
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
            custo = input("Custo de exposição por mês: ")

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

    if operacao == 2:
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
                print(linha)
        else:
            print("\n Nenhum resultado encontrado")
        
        input("\nPressione ENTER para continuar...")

conn.close()
