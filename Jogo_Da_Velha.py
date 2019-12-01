# Integrantes:
# Alisson Eduardo
# Felipe Rodrigues
# Jadson Luciano
# Código com min-max e poda alfabeta

import random
from pip._vendor.distlib.compat import raw_input


def obter_copia_tabuleiro(tabuleiro):
    tabuleiro_copiado = []

    for i in tabuleiro:
        tabuleiro_copiado.append(i)
    return tabuleiro_copiado


def desenhar_tabuleiro(tabuleiro):
    copia_tabuleiro = obter_copia_tabuleiro(tabuleiro)

    for i in range(1, 10):
        if tabuleiro[i] == '':
            copia_tabuleiro[i] = str(i)
        else:
            copia_tabuleiro[i] = tabuleiro[i]

    print("\n")
    print(' ' + copia_tabuleiro[7] + '  |  ' + copia_tabuleiro[8] + '  |  ' + copia_tabuleiro[9])
    print('---------------')
    print(' ' + copia_tabuleiro[4] + '  |  ' + copia_tabuleiro[5] + '  |  ' + copia_tabuleiro[6])
    print('---------------')
    print(' ' + copia_tabuleiro[1] + '  |  ' + copia_tabuleiro[2] + '  |  ' + copia_tabuleiro[3])
    print("\n")


def retornar_letra_jogador():
    letra = ''
    while letra != 'X' and letra != 'O':
        print(' \nAntes de tudo, defina qual é a sua peça: O ou X?')
        letra = raw_input().upper()
        if letra != 'X' and letra != 'O':
            print("\nOpção inválida! \n"
                  "Entre apenas com a letra 'X' se você quer ser 'X'\n "
                  "ou com a letra 'O' se você quer ser 'O'!")

    if letra == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def joga_primeiro():
    if random.randint(0, 1) == 0:
        return 'computador'
    else:
        return 'jogador'


def realizar_movimento(tabuleiro, letra, movimento):
    tabuleiro[movimento] = letra


def ganhador(brd, let):
    return ((brd[7] == let and brd[8] == let and brd[9] == let) or
            (brd[4] == let and brd[5] == let and brd[6] == let) or
            (brd[1] == let and brd[2] == let and brd[3] == let) or
            (brd[7] == let and brd[4] == let and brd[1] == let) or
            (brd[8] == let and brd[5] == let and brd[2] == let) or
            (brd[9] == let and brd[6] == let and brd[3] == let) or
            (brd[7] == let and brd[5] == let and brd[3] == let) or
            (brd[9] == let and brd[5] == let and brd[1] == let))


def espaco_livre(tabuleiro, movimento):
    if tabuleiro[movimento] == '':
        return True
    else:
        return False


def obter_movimento_jogador(tabuleiro):
    movimento = ''
    while movimento not in '1 2 3 4 5 6 7 8 9'.split() or not espaco_livre(tabuleiro, int(movimento)):
        print('\nQual é o seu próximo movimento? Escolha um dos números\n '
              'do tabuleiro acima (1 a 9).')
        movimento = raw_input();
        if movimento not in '1 2 3 4 5 6 7 8 9':
            print("\nOps, valor inválido!! Escolha um dos números acima\n "
                  "de 1 a 9.")

        if movimento in '1 2 3 4 5 6 7 8 9':
            if not espaco_livre(tabuleiro, int(movimento)):
                print("\nEsse espaço já foi ocupado! \n"
                      "Escolha outro espeço entre 1 a 9, com base nos nº\n"
                      " disponiveis no quadro acima.")

    return int(movimento)


def escolher_movimento_aleatorio(tabuleiro, lista_movimentos):
    possiveis_movimentos = []
    for i in lista_movimentos:
        if espaco_livre(tabuleiro, i):
            possiveis_movimentos.append(i)

    if len(possiveis_movimentos) != 0:
        return random.choice(possiveis_movimentos)
    else:
        return None


def tabuleiro_cheio(tabuleiro):
    for i in range(1, 10):
        if espaco_livre(tabuleiro, i):
            return False
    return True


def possiveis_opcoes(tabuleiro):
    opcoes = []

    for i in range(1, 10):
        if espaco_livre(tabuleiro, i):
            opcoes.append(i)
    return opcoes


def finalizar_jogo(tabuleiro, letra_computador):
    if letra_computador == 'X':
        letra_jogador = 'O'
    else:
        letra_jogador = 'X'

    if ganhador(tabuleiro, letra_computador):
        return 1

    elif ganhador(tabuleiro, letra_jogador):
        return -1

    elif tabuleiro_cheio(tabuleiro):
        return 0

    else:
        return None


# -----------------------------------------------------------------------------------------------------------------------
# SERÁ FEITA AQUI A PODA ALFABETA
def alphabeta(tabuleiro, letra_computador, rodada, alpha, beta):
    if letra_computador == 'X':
        letra_jogador = 'O'
    else:
        letra_jogador = 'X'

    if rodada == letra_computador:
        proxima_rodada = letra_jogador
    else:
        proxima_rodada = letra_computador

    fim = finalizar_jogo(tabuleiro, letra_computador)

    if fim is not None:
        return fim

    movimentos_possiveis = possiveis_opcoes(tabuleiro)

    if rodada == letra_computador:
        for movimento in movimentos_possiveis:
            realizar_movimento(tabuleiro, rodada, movimento)
            val = alphabeta(tabuleiro, letra_computador, proxima_rodada, alpha, beta)
            realizar_movimento(tabuleiro, '', movimento)
            if val > alpha:
                alpha = val

            if alpha >= beta:
                return alpha
        return alpha

    else:
        for movimento in movimentos_possiveis:
            realizar_movimento(tabuleiro, rodada, movimento)
            val = alphabeta(tabuleiro, letra_computador, proxima_rodada, alpha, beta)
            realizar_movimento(tabuleiro, '', movimento)
            if val < beta:
                beta = val

            if alpha >= beta:
                return beta
        return beta


def obter_movimento_computador(tabuleiro, letra_computador):
    a = -2
    opcoes = []

    if letra_computador == 'X':
        letra_jogador = 'O'
    else:
        letra_jogador = 'X'

    # -----------------------------------------------------------------------------------------------------------------------
    # SERÁ FEITO AQUI O MINMAX
    # 1) A maquina pode ganhar no próximo movimento.

    for i in range(1, 10):
        copy = obter_copia_tabuleiro(tabuleiro)
        if espaco_livre(copy, i):
            realizar_movimento(copy, letra_computador, i)
            if ganhador(copy, letra_computador):
                return i

    # 2) O jogador pode ganhar no próximo movimento.

    for i in range(1, 10):
        copy = obter_copia_tabuleiro(tabuleiro)
        if espaco_livre(copy, i):
            realizar_movimento(copy, letra_jogador, i)
            if ganhador(copy, letra_jogador):
                return i

    possiveis_opcoes_on = possiveis_opcoes(tabuleiro)

    for movimento in possiveis_opcoes_on:

        realizar_movimento(tabuleiro, letra_computador, movimento)
        val = alphabeta(tabuleiro, letra_computador, letra_jogador, -2, 2)
        realizar_movimento(tabuleiro, '', movimento)

        if val > a:
            a = val
            opcoes = [movimento]

        elif val == a:
            opcoes.append(movimento)

    return random.choice(opcoes)


print('-------------------------------------------------------')
print(' 				 	JOGO DA VELHA 	     			  ')
print('-------------------------------------------------------')

print('                    X  |  O  |                        ')
print('                  -----------------                   ')
print('                       |  X  |                        ')
print('                  -----------------                   ')
print('                    O  |  O  |  X                     ')

print('-------------------------------------------------------')

print('Esse é o JOGO DA VELHA, e o seu objetivo é:\n'
      'formar trincas de um mesmo símbolo. Mas, neste caso,\n'
      'vence quem conseguir formar o maior número de trincas.')

print('\n                 Agora é com vocês!!                 ')

print('-------------------------------------------------------')

jogar = True
while jogar:

    tabuleiro = [''] * 10
    letra_jogador, letra_computador = retornar_letra_jogador()
    rodada = joga_primeiro()
    print('O ' + rodada + ' faz a primeira jogada.\n')
    jogo_comecado = True

    while jogo_comecado:
        if rodada == 'jogador':

            desenhar_tabuleiro(tabuleiro)
            movimento = obter_movimento_jogador(tabuleiro)
            realizar_movimento(tabuleiro, letra_jogador, movimento)

            if ganhador(tabuleiro, letra_jogador):
                desenhar_tabuleiro(tabuleiro)
                print('\nUhuuuuuul! Você venceu o jogo, miserável!')
                jogo_comecado = False

            else:
                if tabuleiro_cheio(tabuleiro):
                    desenhar_tabuleiro(tabuleiro)
                    print('\nIxi, empate! Parece que deu ruim para\n'
                          'os dois jogadores.')
                    break
                else:
                    rodada = 'computador'

        else:

            movimento = obter_movimento_computador(tabuleiro, letra_jogador)
            realizar_movimento(tabuleiro, letra_computador, movimento)

            if ganhador(tabuleiro, letra_computador):
                desenhar_tabuleiro(tabuleiro)
                print("\nEita! Lemento, mas o computador venceu\n"
                      "dessa vez. Tente novamente!!!")
                jogo_comecado = False

            else:
                if tabuleiro_cheio(tabuleiro):
                    desenhar_tabuleiro(tabuleiro)
                    print('\nIxi, empate! Parece que deu ruim para\n'
                          ' os dois jogadores.')
                    break
                else:
                    rodada = 'jogador'

    opcao = ''
    while not (opcao == 'S' or opcao == 'N'):
        print("\nFim de jogo. \n\n"
              '-------------------------------------------------------\n'
              "Você deseja jogar novamente? \n"
              "Para sim digite 'S', para não digite 'N'.")

        opcao = raw_input().upper()
        if opcao != 'S' and opcao != 'N':
            print("\nVocê digitou um valor inválido. \n"
                  "Para sim digite 'S', para não digite 'N'!")

        if opcao == 'N':
            print("\nTe aguardamos até a próxima!")
            jogar = False
