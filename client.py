
import urllib.request
import sys
import random
import time
from math import inf
import copy

# Returns a list of positions available on a board
def get_available_moves(board):
    l = []
    
    #Descomentar proximas linhas para fazer o sanduiche

    #removal_options = self.can_remove(self.player)
    #if removal_options != None:
    #    self.waiting_removal = True
    #    return removal_options
    #else:
    for column in range(len(board)):
        for line in range(len(board[column])):
            if board[column][line] == 0:
                #if (column + 1, line + 1) != forbidden_moves:
                l.append((column + 1, line + 1))
    return l

# Check if a board is in an end-game state. Returns the winning player or None.
def is_final_state(board):
    # test vertical
    for column in range(len(board)):
        s = ""
        for line in range(len(board[column])):
            state = board[column][line]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2

    # test upward diagonals
    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2
            coords = neighbors(board, column, line)[1]

    # test downward diagonals
    diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2
            coords = neighbors(board, column, line)[4]

    return None


# Get a fixed-size list of neighbors: [top, top-right, top-left, down, down-right, down-left].
# None at any of those places where there's no neighbor
def neighbors(board, column, line):
    l = []

    if line > 1:
        l.append((column, line - 1))  # up
    else:
        l.append(None)

    if (column < 6 or line > 1) and (column < len(board)):
        if column >= 6:
            l.append((column + 1, line - 1))  # upper right
        else:
            l.append((column + 1, line))  # upper right
    else:
        l.append(None)
    if (column > 6 or line > 1) and (column > 1):
        if column > 6:
            l.append((column - 1, line))  # upper left
        else:
            l.append((column - 1, line - 1))  # upper left
    else:
        l.append(None)

    if line < len(board[column - 1]):
        l.append((column, line + 1))  # down
    else:
        l.append(None)

    if (column < 6 or line < len(board[column - 1])) and column < len(board):
        if column < 6:
            l.append((column + 1, line + 1))  # down right
        else:
            l.append((column + 1, line))  # down right
    else:
        l.append(None)

    if (column > 6 or line < len(board[column - 1])) and column > 1:
        if column > 6:
            l.append((column - 1, line + 1))  # down left
        else:
            l.append((column - 1, line))  # down left
    else:
        l.append(None)

    return l

def heuristic(board, player):
    #Heuristica dá peso negativo se não é mais possível ganhar na coluna
    
    for col in range(0, len(board)):
        #for l in range(0, len(board[col])):
        if player == "1":
            if board[col].count(1) + board[col].count(0) >= 5:
                return 10 #positivo, segue por aqui
            else:
                return -10 #negativo
        if player == "2":
            if board[col].count(1) + board[col].count(0) >= 5:
                return -10 #positivo, segue por aqui
            else:
                return 10 #negativo
            


def minimax(board, depth, player, depth_initial): 
    """ 
    Minimax algorithm that choose the best movement in board
    Args:
        board (list): the state of the board
        depth (int): how many free position the board has
        player (str): player ("X" or "O") 
    Returns:
        tuple: score and best move
    """

    h = heuristic(board, player)

    final_state = is_final_state(board)
    if final_state is not None:
        if final_state == 1:
            return -10 - depth, board
        else:
            return 10 + depth, board
    if depth == depth_initial-2:
        return h, board 
    #print(player)
    #print("BOARD")
    #print(board)
    #print("MOVE")

    if player == "2":
        best_val = -inf
        best_mov = None
        for move in get_available_moves(board):
            #print(move)
            #print(get_available_moves(board))
            board_cpy = copy.deepcopy(board)
            column, line = move
            board_cpy[column-1][line-1] = 2
            #print(board_cpy)
            value, mov = minimax(board_cpy, depth-1, "1", depth_initial)
            if best_val < value:
                best_val = value
                best_mov = move
        return best_val, best_mov
    
    else:
        best_val = inf
        best_mov = None
        for move in get_available_moves(board):
            #print(move)
            #print(get_available_moves(board))
            board_cpy = copy.deepcopy(board)
            column, line = move
            board_cpy[column-1][line-1] = 1
            #print(board_cpy)
            value, mov = minimax(board_cpy, depth-1, "2", depth_initial)
            if best_val > value:
                best_val = value
                best_mov = move
        return best_val, best_mov



if len(sys.argv)==1:
    print("Voce deve especificar o numero do jogador (1 ou 2)\n\nExemplo:    ./random_client.py 1")
    quit()

# Alterar se utilizar outro host
host = "http://localhost:8080"

player = int(sys.argv[1])

# Reinicia o tabuleiro
resp = urllib.request.urlopen("%s/reiniciar" % host)

done = False
    

while not done:
    # Pergunta quem eh o jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())

    # Se jogador == 0, o jogo acabou e o cliente perdeu
    if player_turn==0:
        print("I lose.")
        done = True

    # Se for a vez do jogador
    if player_turn==player:
        time.sleep(1)
        # Pega os movimentos possiveis
        resp = urllib.request.urlopen("%s/movimentos" % host)
        movimentos = eval(resp.read())

        #Pega o tabuleiro completo
        resp = urllib.request.urlopen("%s/tabuleiro" % host)
        board = eval(resp.read()) #lista com 11 listas representando cada fileira na vertical (0 vazio, 1 player 1 e 2 player 2)

        # Escolhe um movimento aleatoriamente
        #movimento = random.choice(movimentos)
        movimento = minimax(board, len(movimentos), str(player), len(movimentos))
        print(movimento)
        #print(movimento[1][0])
        #print(movimento[1][1])
        # Executa o movimento
        resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[1][0],movimento[1][1]))
        msg = eval(resp.read())

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])
    
    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)


