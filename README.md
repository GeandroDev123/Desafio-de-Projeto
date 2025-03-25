﻿# Calculadora-de-partidas

 # Solicita entrada do usuário
quantidade_partidas = int(input("Digite a quantidade de partidas: "))
vitorias = int(input("Digite a quantidade de vitórias: "))
derrotas = int(input("Digite a quantidade de derrotas: "))

# Função para calcular saldo de vitórias e definir nível do jogador
def saldo_de_vitorias(vitorias, derrotas):
    saldo = vitorias - derrotas  # Calcula saldo de vitórias

    # Classificador de vitórias
    if vitorias <= 10:
        nivel = "Ferro"
    elif 11 <= vitorias <= 20:
        nivel = "Bronze"
    elif 21 <= vitorias <= 50:
        nivel = "Prata"
    elif 51 <= vitorias <= 80:
        nivel = "Ouro"
    elif 81 <= vitorias <= 90:
        nivel = "Diamante"
    elif 91 <= vitorias <= 100:
        nivel = "Lendário"
    else:
        nivel = "Imortal"

    return saldo, nivel  # Retorna saldo e nível

# Chama a função e armazena os resultados
saldo, nivel = saldo_de_vitorias(vitorias, derrotas)

# Exibe o resultado final
print(f"O Herói tem um saldo de {saldo} e está no nível {nivel}.")
