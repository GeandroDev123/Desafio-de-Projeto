import sqlite3

# Função para conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('sistema_plotter.db')
    cursor = conn.cursor()
    return conn, cursor  # Retorna a conexão e o cursor

# Função para criar tabelas
def criar_tabelas():
    conn, cursor = conectar_banco()  # Obtém a conexão e o cursor

    # Criando tabela produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        codigo TEXT PRIMARY KEY,
        descricao TEXT NOT NULL,
        cliente TEXT,
        unidade TEXT,
        navalha TEXT,
        modelo TEXT,
        status TEXT DEFAULT 'ATIVO'
    )
    ''')

    # Criando tabela pedidos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE,
        numero_do_pedido INTEGER,
        cliente TEXT,
        codgio INTEGER,
        produto TEXT,
        quantidade INTEGER,
        data_de_entrega DATE,
        projecao_de_placas FLOAT,
        FOREIGN KEY (produto) REFERENCES produtos(codigo)
    )
    ''')

    # Criando tabela producao 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS producao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_inicial DATE,
        pedido INTEGER,
        cliente TEXT,
        codigo INTEGER,
        produto TEXT,
        hora_inicio TIME,
        hora_final TIME,
        data_final DATE,
        quantidade_produzida INTEGER,
        quantidade_esperada INTEGER,
        status TEXT,
        placas_utilizadas INTEGER,
        sobras_placas INTEGER,
        media_pares_por_placa REAL,
        FOREIGN KEY (produto) REFERENCES produtos(codigo)
    )
    ''')

    # Salva e fecha a conexão
    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso!")

# Executar a criação das tabelas
criar_tabelas()

# Função para adicionar um produto
def adicionar_produto(cursor, conn):
    codigo = input("Digite o código do produto: ")
    descricao = input("Digite o nome do produto: ")
    cliente = input("Digite o nome do cliente: ")
    unidade_de_medida = input("Digite a unidade de medida: ")
    navalha = input("Digite a navalha: ")
    modelo = input("Digite o modelo: ")

    cursor.execute("SELECT * FROM produtos WHERE codigo = ?", (codigo,))
    if cursor.fetchone():
        print(f"Erro: o produto com código {codigo} já existe no sistema.")
        return

    cursor.execute('''
    INSERT INTO produtos (codigo, descricao, cliente, unidade, navalha, modelo)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (codigo, descricao, cliente, unidade_de_medida, navalha, modelo))
    conn.commit()
    print(f'Produto "{descricao}" adicionado com sucesso!')

# Função para editar produto
def editar_produto(cursor, conn):
    codigo = input("Digite o código do produto que deseja editar: ")
    cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (codigo,))
    produto = cursor.fetchone()

    if produto:
        nova_descricao = input(f"Digite a nova descrição para {produto[1]}: ")
        novo_cliente = input(f"Digite o novo cliente para {produto[1]}: ")
        nova_unidade = input(f"Digite a nova unidade para {produto[1]}: ")
        nova_navalha = input(f"Digite a nova navalha para {produto[1]}: ")
        novo_modelo = input(f"Digite o novo modelo para {produto[1]}: ")

        cursor.execute('''
        UPDATE produtos
        SET descricao = ?, cliente = ?, unidade = ?, navalha = ?, modelo = ?
        WHERE codigo = ?
        ''', (nova_descricao, novo_cliente, nova_unidade, nova_navalha, novo_modelo, codigo))
        conn.commit()
        print(f"Produto {produto[1]} atualizado com sucesso!")
    else:
        print(f"Produto com o código {codigo} não encontrado.")

# Função para listar produtos
def listar_produtos(cursor):
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    if produtos:
        print("\nLista de produtos cadastrados:")
        print("=".center(30, "="))
        for produto in produtos:
            print(f"Código: {produto[0]}, Descrição: {produto[1]}, Cliente: {produto[2]}, Unidade: {produto[3]}, Navalha: {produto[4]}, Modelo: {produto[5]}")
        print("=" * 30)
    else:
        print("Nenhum produto cadastrado.")


import sqlite3
from datetime import datetime

# Função para obter a data atual
def obter_data_atual():
    return datetime.now().strftime("%d/%m/%Y")

# Função para adicionar um pedido manualmente
def adicionar_pedido(cursor, conn):
    """
    Adiciona um pedido na tabela 'pedidos', permitindo pedidos repetidos.
    A data é gerada automaticamente.
    """
    data_atual = obter_data_atual()
    numero_do_pedido = input("Digite o número do pedido: ").strip()

    try:
        cursor.execute('''
        INSERT INTO pedidos (data, pedido)
        VALUES (?, ?)
        ''', (data_atual, numero_do_pedido))

        conn.commit()
        print(f"Pedido '{numero_do_pedido}' registrado com sucesso na data {data_atual}!")
    except sqlite3.Error as e:
        print(f"Erro ao registrar pedido: {e}")

# Função para adicionar pedido por código do produto
def adicionar_pedido_por_codigo(cursor, conn):
    """
    Busca cliente e produto na tabela 'produtos' a partir do código
    e insere automaticamente esses dados na tabela 'pedidos'.
    """
    codigo = input("Digite o código do produto: ").strip()

    cursor.execute('SELECT cliente, descricao FROM produtos WHERE codigo = ?', (codigo,))
    produto = cursor.fetchone()

    if produto:
        cliente, descricao = produto
        print(f"Produto encontrado! Cliente: {cliente}, Produto: {descricao}")

        try:
            cursor.execute('''
            INSERT INTO pedidos (data, cliente, produto)
            VALUES (?, ?, ?)
            ''', (obter_data_atual(), cliente, descricao))

            conn.commit()
            print(f"Pedido para o cliente '{cliente}' e produto '{descricao}' foi inserido com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao inserir pedido: {e}")
    else:
        print(f"Nenhum produto encontrado com o código {codigo}.")

# Função para adicionar quantidade e data de entrega ao pedido
def quantidade_do_pedido(cursor, conn):
    """
    Adiciona a quantidade do pedido na tabela 'pedidos'.
    Também solicita e insere a data de entrega do pedido.
    """
    try:
        quantidade = int(input("Digite a quantidade do pedido: ").strip())
    except ValueError:
        print("Erro: A quantidade deve ser um número inteiro.")
        return

    data_de_entrega = input("Digite a data de entrega do pedido (DD/MM/YYYY): ").strip()

    try:
        cursor.execute('''
            INSERT INTO pedidos (data, quantidade)
            VALUES (?, ?)
        ''', (data_de_entrega, quantidade))

        conn.commit()
        print(f"Pedido de {quantidade} unidades registrado com sucesso para entrega em {data_de_entrega}!")
    except sqlite3.Error as e:
        print(f"Erro ao registrar a quantidade do pedido: {e}")

# Função para calcular a projeção de placas
def calcular_projecao(cliente, quantidade):
    """
    Calcula a projeção de placas com base no cliente e na quantidade do pedido.
    """
    try:
        quantidade = float(quantidade)
    except ValueError:
        return "Erro: A quantidade deve ser um número."

    clientes = {
        "Coopershoes": 73,
        "Dakota": 80,
        "Dass": 70
    }

    if cliente in clientes:
        projecao = quantidade / clientes[cliente]
        return f"Projeção de placas para {cliente}: {projecao:.2f} placas."
    else:
        return "Erro: Cliente não encontrado na base de cálculos."

# Configuração do sistema de logs
import logging

# Configuração do sistema de logs
logging.basicConfig(filename='sistema.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def calcular_projecao(cliente, quantidade):
    divisores = {"Coopershoes": 73, "Dakota": 80, "Dass": 70}
    divisor = divisores.get(cliente)

    if divisor:
        projecao = quantidade / divisor
        logging.info(f"Projeção calculada: Cliente={cliente}, Quantidade={quantidade}, Placas={projecao:.2f}")
        return f"Projeção de placas para {cliente}: {projecao:.2f} placas."
    else:
        logging.error(f"Cliente {cliente} não encontrado para projeção.")
        return "Erro: Cliente não encontrado."

"clientes.json"

{
    "Coopershoes": 73,
    "Dakota": 80,
    "Dass": 70,
    "Topshoes": 35
}

import json

def carregar_divisores():
    """Lê os divisores do arquivo JSON apenas uma vez"""
    try:
        with open("clientes.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Carregar divisores uma única vez
divisores = carregar_divisores()
print(divisores)

def calcular_projecao(cliente, quantidade):
    """Calcula a projeção de placas para um cliente específico"""
    divisor = divisores.get(cliente)  # Pega o divisor do cliente

    if divisor is not None:  
        projecao = quantidade / divisor
        return f"Projeção de placas {cliente}: {projecao:.2f} placas."
    else:
        return "Erro: Cliente não encontrado."

def adicionar_cliente(nome_cliente, divisor):
    """Adiciona um novo cliente ao arquivo JSON"""
    try:
        with open("clientes.json", "r") as file:
            dados = json.load(file)
    except FileNotFoundError:
        dados = {}

    dados[nome_cliente] = divisor

    with open("clientes.json", "w") as file:
        json.dump(dados, file, indent=4)

    print(f"Cliente '{nome_cliente}' adicionado com sucesso!")

# Testes rápidos
print(calcular_projecao("Coopershoes", 100))
adicionar_cliente("Topshoes", 35)

# Produção da Plotter

import sqlite3
from datetime import datetime

# Função para adicionar data inicial 
def data_inicial(cursor, conn):
    while True:
        data_input = input("Digite a data inicial de corte do pedido (DD/MM/YYYY): ").strip()

        try:
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y").strftime("%Y-%m-%d")

            cursor.execute('''
            INSERT INTO producao (data_inicial)
            VALUES(?)
            ''',(data_formatada,))

            conn.commit()
            print(f"Data inicial registrada com sucesso em {data_formatada}!")
            break
        except ValueError:
            print("Formato inválido! Digite a data no formato DD/MM/YYYY.")

        except sqlite3.Error as e:
            print(f"Erro ao registrar a data inicial no banco:{e}")
            break

# Função para adicionar pedido na tabela produção
import sqlite3

def adicionar_pedido(cursor, conn):
    """
    Busca número do pedido na tabela 'pedidos' e insere automaticamente esses dados na tabela 'producao'.
    """

    # Solicita o número do pedido ao usuário
    numero_pedido = input("Digite o número do pedido: ").strip()

    try:
        # Busca o pedido no banco de dados
        cursor.execute('''
            SELECT cliente, codigo, produto, quantidade FROM pedidos WHERE numero_do_pedido = ?
        ''', (numero_pedido,))

        dados_pedido = cursor.fetchone()  # Obtém os dados encontrados

        if dados_pedido:
            cliente, codigo, nome_produto, quantidade = dados_pedido  # Renomeando `produto` para `nome_produto`

            print(f"Pedido encontrado! Cliente: {cliente}, Código: {codigo}, Produto: {nome_produto}, Quantidade: {quantidade}")

            # Insere os dados na tabela 'producao'
            cursor.execute('''
                INSERT INTO producao (cliente, codigo, produto, quantidade_esperada)
                VALUES (?, ?, ?, ?)
            ''', (cliente, codigo, nome_produto, quantidade))

            conn.commit()
            print(f"Pedido do cliente '{cliente}' e produto '{nome_produto}' foi inserido com sucesso na produção!")

        else:
            print(f"Nenhum pedido encontrado com o número {numero_pedido}.")

    except sqlite3.Error as e:
        print(f"Erro ao inserir pedido no banco de dados: {e}")

           
    from datetime import datetime

    # Função para adicionar hora inicial corte na tabela produção
    def obter_hora_inicial ():

        # Solicita hora inicial do corte ao usuário
        while True:
            hora_inicial = input("Digite a hora inicial de corte (HH:MM):").strip()
            try:
                hora_formatada = datetime.strptime(hora_inicial,"%H:%M").strftime("%H:%M")
                return hora_formatada
            except ValueError:
                print("Formato inválido! Digite a hora no formato HH:MM.")



        # Exemplo de uso
    hora = obter_hora_inicial()
    print(f"Hora inicial registrada: {hora}")

    
    from datetime import datetime

    # Função para adicionar hora final de corte na tabela produção
    def obter_hora_final ():

        # Solicita hora inicial do corte ao usuário
        while True:
            obter_hora_final = input("Digite a hora final de corte (HH:MM):").strip()
            try:
                hora_formatada = datetime.strptime(obter_hora_final,"%H:%M").strftime("%H:%M")
                return hora_formatada
            except ValueError:
                print("Formato inválido! Digite a hora no formato HH:MM.")



        # Exemplo de uso
    hora = obter_hora_final()
    print(f"Hora final registrada: {hora}")



       









       







    

   
        


    


    

        


   




    









        






    

