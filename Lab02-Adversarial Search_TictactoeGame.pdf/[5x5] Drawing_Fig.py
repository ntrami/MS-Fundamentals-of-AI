import copy
import sys
from tkinter import S
from turtle import Screen
import pygame
import random
import numpy as np

# from tictactoe import CIRC_COLOR

# from tictactoe import Board


WIDTH = 600
HEIGHT = 600

ROWS = 5
COLS = 5
SQSIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 10
CROSS_WIDTH = 15

RADIUS = SQSIZE // 4
OFFSET = 30

# COLORS
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRC_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE MINIMAX')
screen.fill( BG_COLOR )

class Board():
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        # self.empty_sqr = self.squares # [squares]
        self.marked_sqrs = 0
        # self.mark_sqr(2, 3, 1)
        # print(self.squares)
    '''
    def final_state(self):
        
        # @return 0 if there is no win yet
        # @return 1 if player 1 wins
        # @return 2 if player 2 wins
        
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        
        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]

        # no win yet
        return 0
        '''
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        # self.marked_sqrs += 1
    
    def empty_sqr(self, row, col):
        print("test: ", self.squares[row][col] == 0)
        return self.squares[row][col] == 0 
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0 

class Game:
    def __init__(self):
        self.board = Board()
        # self.ai = AI()
        self.player = 1 #1-cross #2-circle
        # self.gamemode = 'pvp' # pvp or ai
        # self.running = True
        self.show_lines()
    def show_lines(self):
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE*2, 0), (WIDTH - SQSIZE*2, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE*3, 0), (WIDTH - SQSIZE*3, HEIGHT), LINE_WIDTH)
        
        # horizantal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE*2), (WIDTH, HEIGHT - SQSIZE*2), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE*3), (WIDTH, HEIGHT - SQSIZE*3), LINE_WIDTH)
    
    def next_turn(self):
        self.player = self.player % 2 + 1  # change player 1 | 2

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col*SQSIZE+OFFSET, row*SQSIZE+OFFSET)
            end_desc = (col*SQSIZE + SQSIZE - OFFSET, row*SQSIZE+SQSIZE-OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col*SQSIZE+OFFSET, row*SQSIZE+SQSIZE-OFFSET)
            end_asc = (col*SQSIZE+SQSIZE-OFFSET, row*SQSIZE+OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        elif self.player == 2:
            # draw circle
            center = (col*SQSIZE+SQSIZE//2, row*SQSIZE+SQSIZE//2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)



def main():

    # object
    game = Game()
    board = game.board

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN: # Get postion of mouse click
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()
                    print(board.squares)

                # game.board.mark_sqr(row, col, 1) # Mark rows which was visited
                # print(game.board.squares)
                # print(row, col)
                # print(event.pos)
        pygame.display.update()

main()