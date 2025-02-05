import pygame, sys
import GameEngine as Engine
from UserInterface import *
from Const import *
import AI
import time

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Domineering')      #naziv prozora
Icon = pygame.image.load('images/logo.png')     #logo igrice/prozora
pygame.display.set_icon(Icon)
    
def resetGame(Field):
    pygame.display.set_caption('Domineering')   #naziv prozora
    Field = Engine.CreateMatrix(ROWS,COLS)      #resetujemo matricu
    Engine.CountMove = 1                        #resetujemo brojac poteza
    mainLoop()                                  #crtamo tablu i igrace iznova

def mainLoop():
    Field = Engine.CreateMatrix(ROWS,COLS)
    playerOnMove = 1
    global screen
    
    gameFinished = False

    while True:
        show_bg(screen, Field)
        if gameFinished: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            continue #samo crtaj tablu kad se zavrsi game

        #variables
        newMoveRow = 0
        newMoveCol = 0
        moveReady = False

        #AI turn
        if playerOnMove == AI_TURN:
            start = time.time()

            aiTurn = AI.getNextMoveMinMax(Field, getDepth(Engine.CountMove), playerOnMove)

            end = time.time()
            print("time needed for AI turn: ", end - start, "s")
            newMoveRow = aiTurn[0]
            newMoveCol = aiTurn[1]
            print(aiTurn)
            moveReady = True
        #Human turn
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    newMoveCol = location[0]//SQSIZE # x koordinata pozicije klika
                    newMoveRow = location[1]//SQSIZE # y koordinata pozicije klika
                    if Engine.isMoveValid(newMoveRow, newMoveCol, Field, playerOnMove):
                        moveReady = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:                       
                        resetGame(Field)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        
        if moveReady:
            Engine.placeDomino(newMoveRow, newMoveCol, Field, playerOnMove)
            print(playerOnMove)
            Engine.PrintField(Field)
            playerOnMove = Engine.getNextPlayer(playerOnMove)
            Engine.RaiseCounter()
            
            if Engine.getAvailableMovesNumber(Field, playerOnMove) == 0:
                PlayerWonAlert(playerOnMove%2+1)
                show_bg(screen, Field)                
                gameFinished = True                           

        #Hover za human turn
        location = pygame.mouse.get_pos()
        col = location[0]//SQSIZE
        row = location[1]//SQSIZE
        if playerOnMove==1:
            HoverPlayerOne(row, col, Field, screen)
        elif playerOnMove==2:
            HoverPlayerTwo(row, col, Field, screen)
        pygame.display.update()

mainLoop()