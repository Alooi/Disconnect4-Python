from random import randint
import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def calculate_score(board, row, col, piece, player):
	c, r = col+1, row+1
	max_k = 0
	k = 0
	# check diagonal
	while c < COLUMN_COUNT and r < ROW_COUNT:
		if board[r][c] == piece:
			k += 1
			if k > max_k:
				max_k = k
		else:
			break
		c += 1
		r += 1
	c, r = col-1, row-1
	while c >= 0 and r >= 0:
		if board[r][c] == piece:
			k += 1
			if k > max_k:
				max_k = k
		else:
			if k > max_k:
				max_k = k
			break
		c -= 1
		r -= 1
	c, r = col+1, row-1
	k = 0
	while c < COLUMN_COUNT and r >= 0:
		if board[r][c] == piece:
			k += 1
			if k > max_k:
				max_k = k
		else:
			if k > max_k:
				max_k = k
			break
		c += 1
		r -= 1
	c, r = col-1, row+1
	while c >= 0 and r < ROW_COUNT:
		if board[r][c] == piece:
			k += 1
			if k > max_k:
				max_k = k
		else:
			if k > max_k:
				max_k = k
			break
		c -= 1
		r += 1
	print('diagonal score', k+1)
	#check horizontal
	c, r = col+1, row
	k = 0
	while c < COLUMN_COUNT:
		if board[r][c] == piece:
			k += 1
			if k > max_k:
				max_k = k
		else:
			if k > max_k:
				max_k = k
			break
		c += 1
	c, r = col-1, row
	while c >= 0:
		if board[r][c] == piece:
			k += 1
			if k > max_k:
				max_k = k
		else:
			if k > max_k:
				max_k = k
			break
		c -= 1
	print('horizontal score', k+1)
	#check vertical 
	c, r = col, row-1
	k = 0
	while r < ROW_COUNT:
		if board[r][c] == piece:
			k += 1
			if k > max_k:
				max_k = k
		else:
			if k > max_k:
				max_k = k
			break
		r -= 1
	max_k += 1
	print('vertical score', k+1)
	print('play score:', max_k)
	return max_k

def add_score(score, player):
	if player == 1:
		PLAYER_1_SCORE += score
	else:
		PLAYER_2_SCORE += score

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def take_piece(board, col, player):
	row = ROW_COUNT -1
	piece = 0
	while row >= 0:
		if board[row][col] != 0:
			piece = int(board[row][col])
			board[row][col] = 0
			print('removed piece', piece ,'from', row, col)
			# TODO calculate score here, using (player, piece, row, col). That is all information needed for score
			calculate_score(board, row, col, piece, player)
			break
		row -= 1

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))


def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

def fill_board(board):
	turn = 0
	pieces = 0
	board_size = COLUMN_COUNT * ROW_COUNT
	while pieces != board_size:	
		turn += 1
		col = randint(0,COLUMN_COUNT-1)
		if is_valid_location(board, col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, turn)
			pieces += 1
		turn -= 1
		turn += 1
		turn = turn % 2

fill_board(board)
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


# We can ignore most of the code below if we were to make both players play automatically, this part of the code is mostly visual for actually playing the game.
while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				# if is_valid_location(board, col):
				# 	row = get_next_open_row(board, col)
				# 	drop_piece(board, row, col, 1)
				take_piece(board, col, 1)

					# if winning_move(board, 1):
					# 	label = myfont.render("Player 1 wins!!", 1, RED)
					# 	screen.blit(label, (40,10))
					# 	game_over = True


			# # Ask for Player 2 Input
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				# if is_valid_location(board, col):
				# 	row = get_next_open_row(board, col)
				# 	drop_piece(board, row, col, piece)
				take_piece(board, col, 2)

					# if winning_move(board, 2):
					# 	label = myfont.render("Player 2 wins!!", 1, YELLOW)
					# 	screen.blit(label, (40,10))
					# 	game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)