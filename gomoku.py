import numpy as np
import copy
import random
import os
from tabulate import tabulate

LINHA = 10
COLUNA = 10

class Tabuleiro:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.matriz = np.zeros((linha,coluna))
        self.jogos = [] # Lista para guardas os estados do jogo
    
    #--------------- RETORNA ESTADO ATUAL DO JOGO --------------
    @property
    def retorna_estado(self):
        return self.matriz
    
    #------------------- FAZ UMA JOGADA -----------------------
    def jogar(self, linha, coluna, jogador):
        self.matriz_copia = copy.deepcopy(self.matriz)
        self.jogos.append(self.matriz_copia) # Cria uma cópia do estado atual e adiciona na lista de estados

        self.jogador = jogador
        if jogador == 'pretas':
            self.matriz[linha - 1, coluna - 1] = 1
        else:
            self.matriz[linha - 1, coluna - 1] = 2

    #------------------- VERIFICA SE JOGADA É VALIDA -----------------------
    def verifica_jogada(self, linha, coluna):
        if (self.matriz[linha-1][coluna-1] == 1 or self.matriz[linha-1][coluna-1] == 2):
            return False
        else:
            return True

        
    '''
    ------------------- IMPRIMI EM FORMA SIMPLES DE MATRIZ ----------------  
    @property
    def imprimir(self):
        print(f'\n{gomoku.retorna_estado}\n')
    '''

    #------------------ iMPRIMI O JOGO COM MATRIZ ESTILIZADA -------------------
    def imprimir_matriz(self):
        # Cria uma lista de listas a partir da matriz numpy
        matriz = self.matriz
        lista = matriz.tolist()

        # Substitui 0 por espaço em branco
        # Substitui 1 por ◻
        # Substitui 2 por ◼
        for i in range(len(lista)):
            for j in range(len(lista[i])):
                if (lista[i][j]) == 0:
                    lista[i][j] = ""
                elif (lista[i][j]) == 1:
                    lista[i][j] = "◻"
                else:
                    lista[i][j] = "◼"

        # Cria uma lista de cabeçalhos para as colunas
        cabecalhos = [""] + [f"{j+1}" for j in range(len(matriz))]

        # Adiciona números de linha a cada lista interna
        for i in range(len(lista)):
            lista[i].insert(0, f"{i+1}")

        # Usa o módulo tabulate para imprimir a tabela com uma formatação estilizada
        print(tabulate(lista, headers=cabecalhos, tablefmt="fancy_grid", stralign='center'))


    #----------------------- VERIFICA SE O JOGADOR GANNHOU -------------------------
    def verifica_se_ganhou(self, peca):
        # Verifica linha
        for i in range(LINHA):
            ganhou = 0
            for j in range(COLUNA):
                if (self.matriz[i][j] == peca):
                    ganhou += 1
                    if (ganhou == 5):
                        return True
                else:
                    ganhou = 0

        # Verifica coluna
        for j in range(COLUNA):
            ganhou = 0
            for i in range(LINHA):
                if (self.matriz[i][j] == peca):
                    ganhou += 1
                    if (ganhou == 5):
                        return True
                else:
                    ganhou = 0

        # Verifica diagonal principal
        ganhou = 0
        for i in range(10):
            if (self.matriz[i][i] == peca):
                ganhou += 1
                if (ganhou == 5):
                    return True
            else:
                ganhou = 0

        # Verifica diagonal secundária
        ganhou = 0
        for i in range(10):
            if (self.matriz[i][j] == peca):
                ganhou += 1
                if (ganhou == 5):
                    return True
                j -= 1
            else:
                ganhou = 0
                j = 9

    #-------- SE A JOGADA FOR VÁLIDA SEGUE, SENÃO O JOGADOR JOGA NOVAMENTE ---------
    def proximo_jogador(self, jogada_valida, jogador):
        if jogada_valida:
            if jogador == 1:
                return 2
            else:
                return 1
        else:
            return jogador 
        
    #----------------- LIMPA O TERMINAL ----------------
    def limpar_tela(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

gomoku = Tabuleiro(LINHA, COLUNA) # Cria Tabuleiro com tamanho desejado
sorteio_jogador = random.randint(1, 2) # 1 - Pretas. 2 - Brancas 

ganhou = False # Alguem ganhou
empate = False # jogo empatado

# Laço acontece enquanto alguem não ganhou ou o jogo não empatou
while (not ganhou and not empate):
    
    gomoku.imprimir_matriz() # Imprimi o jogo na tela

    # Verifica de quem é a vez de jogar e faz a jogada
    if sorteio_jogador == 1:
        print("Jogador 1")
        linha = int(input("Linha: "))
        coluna = int(input("Coluna: "))
        jogada_valida = gomoku.verifica_jogada(linha, coluna)

        #print(f'Jogada foi válida: {jogada_valida}')
        if jogada_valida:
            gomoku.jogar(linha, coluna, "pretas")
    else:
        print("Jogador 2")
        linha = int(input("Linha: "))
        coluna = int(input("Coluna: "))
        jogada_valida = gomoku.verifica_jogada(linha, coluna)
        
        #print(f'Jogada foi válida: {jogada_valida}')
        if jogada_valida:
            gomoku.jogar(linha, coluna, "brancas")
        

    gomoku.limpar_tela() # Limpa o terminal
    
    # Se a jogada for válida, joga o outro jogador. Se for inválida o jogador joga novamente
    sorteio_jogador = gomoku.proximo_jogador(jogada_valida, sorteio_jogador) 

    pretas = gomoku.verifica_se_ganhou(1) # Verifica se as pretas ganharam
    brancas = gomoku.verifica_se_ganhou(2) # Verifica se as brancas ganharam

    ganhou = pretas # Verifica se alguem ganhou
    ganhou = brancas # Verifica se alguem ganhou

    # Verifica se o jogo empatou
    if not 0 in [elemento for linha in gomoku.matriz for elemento in linha]:
        empate = True


gomoku.imprimir_matriz()
if pretas:
    print('JOGADOR 1 GANHOU!')
if brancas:
    print('JOGADOR 2 GANHOU!')
if empate:
    print('O JOGO EMPATOU!')



