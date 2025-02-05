import sys

ROWS = 8 #default values
COLS = 8
AI_TURN = 0 #0=pvp, 1=prvi igra AI, 2=drugi igra AI

#fetch from args
length = len(sys.argv)
if length < 3:
    print("Uneli ste lose argumente! Tabla postavljena na podrazumevanu vrednost 8x8")
if length >= 3:
    if int(sys.argv[1]) > 20 or int(sys.argv[2]) > 20:
        print("Maksimalne dimenzije su 20x20!")
        print("Tabla postavljena na podrazumevanu vrednost 8x8")
    else:
        ROWS = int(sys.argv[1])
        COLS = int(sys.argv[2])
if length >= 4:
        AI_TURN = int(sys.argv[3])
        print("Human vs Computer")

if AI_TURN == 0:
    print("Human vs Human")

WIDTH = COLS * 70
HEIGHT = ROWS * 70
SQSIZE = WIDTH // COLS #square size

TIME_LIMIT_SECONDS = 28 #value - 1

P1_WIN_VALUE = 100
P2_WIN_VALUE = -100

ALPHA_START = -float("inf")
BETA_START = float("inf")

SORT_PRUNE_VAL = 0 #sto blize nuli to je pruning ostriji. theoretical max za value je 16, ali je 99% poteza u okviru 0-1
PRUNING_THRESHOLD = 14 #ako ima vise od ovoliko poteza mogucih, try to prune (ako je mali broj ne kosta nas nista da za sv. slucaj prodjemo sve slucajeve)
#IDEALLY ovo gornje je onk fine tuned na dobar value a ovo dole je 1 (mora da bude preko 0)

START_DEPTH = 4 - AI_TURN #self explainatory

def getDepth(countMove):
    depth = START_DEPTH
    if(countMove>9):
        depth+=2
    if(countMove>11):
        depth+=2
    if(countMove>15):
        depth+=2
    return depth