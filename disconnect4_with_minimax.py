import numpy as np
import random
import pygame
import sys
import math
from random import randint

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

WINDOW_LENGTH = 4

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def calculate_score(board, row, col, piece, player):
	# print('checking column: ', col)
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
	# print('diagonal score', k+1)
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
	# print('horizontal score', k+1)
	#check vertical 
	c, r = col, row-1
	k = 0
	while r > ROW_COUNT:
		if board[r][c] == piece:
			k += 1
			if k > max_k:
				max_k = k
		else:
			if k > max_k:
				max_k = k
			break
		r -= 1
	if (piece != player):
		max_k = -1
	else:
		max_k += 1
	# print('vertical score', k+1)
	# print('play score:', max_k)
	# add_score(max_k, player, piece)
	return max_k

def add_score(score, player, piece):
	global PLAYER_1_SCORE
	global PLAYER_2_SCORE

	if player == 1:
		if piece == player:
			PLAYER_1_SCORE += 1
			PLAYER_2_SCORE -= 1
		else:
			PLAYER_1_SCORE += score
			PLAYER_2_SCORE -= score
	else:
		if piece == player:
			PLAYER_2_SCORE += 1
			PLAYER_1_SCORE -= 1
		else:
			PLAYER_2_SCORE += score
			PLAYER_1_SCORE -= score
	# print('player1 total score: ', PLAYER_1_SCORE)
	# print('player2 total score: ', PLAYER_2_SCORE)


def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	# if col == 0:
	# 	print('column zero validation: ', board[0][col] != 0)
	return board[0][col] != 0

def is_valid_location_fill(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	row = ROW_COUNT-1
	while row >= 0:
		if board[row][col] != 0:
			return row
		row -= 1
	# print('none at column', col)
	# print_board(board)
	return 'dafuq'

def get_next_open_row_fill(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))


def is_terminal_node(board):
	return len(get_valid_locations(board)) == 0

def take_piece(board, col, player):
	row = ROW_COUNT -1
	piece = 0
	while row >= 0:
		# print('board at location:', board[row][col])
		if board[row][col] != 0:
			piece = int(board[row][col])
			board[row][col] = 0
			# calculate_score(board, row, col, piece, player)
			break
		row -= 1

def minimax(board, depth, alpha, beta, maximizingPlayer, piece, column):
	# print('current depth:', depth)
	valid_locations = get_valid_locations(board)
	if get_next_open_row(board, column) == 'dafuq':
		# print('we hit rock bottom at column: ', column)
		return (None, 0)
	is_terminal = is_terminal_node(board)
	if maximizingPlayer:
		player = 2
	else:
		player = 1

	if depth == ROW_COUNT-1 or is_terminal:
		if is_terminal:
			return (None, 0)
		else:
			return (None, calculate_score(board, get_next_open_row(board, column), column, get_piece(board, column), piece))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			# row = get_next_open_row(board, col)
			b_copy = board.copy()
			take_piece(b_copy,col,player)
			new_score = minimax(b_copy, depth+1, alpha, beta, False, AI_PIECE, col)[1]
			if new_score > value:
				value = new_score
				column = col
				# print('found max score at: ', col, ' score: ', new_score)
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		# print('maxinmizing score:', column, value)
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			# row = get_next_open_row(board, col)
			b_copy = board.copy()
			take_piece(b_copy,col,player)
			new_score = minimax(b_copy, depth+1, alpha, beta, True, PLAYER_PIECE, col)[1]
			if new_score < value:
				value = new_score
				column = col
				# print('found min score at: ', col, ' score: ', new_score)
			beta = min(beta, value)
			if alpha >= beta:
				break
		# print('minimizing score:', column, value)
		return column, value

def get_piece(board, col):
	row = ROW_COUNT - 1
	while row >= 0:
		if board[row][col] != 0:
			return int(board[row][col])
		row -= 1


def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
	player = 2
	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		take_piece(temp_board, col, player)
		score = calculate_score(temp_board, row, col, get_piece(board, col), piece)
		if score > best_score:
			best_score = score
			best_col = col
	# print('best score:', best_score, 'at column: ', best_col, 'piece taken out: ', get_piece(board, best_col))
	return best_col, best_score

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
# print_board(board)
game_over = False
def fill_board(board):
	turn = 0
	pieces = 0
	board_size = COLUMN_COUNT * ROW_COUNT
	while pieces != board_size:	
		turn += 1
		col = randint(0,COLUMN_COUNT-1)
		if is_valid_location_fill(board, col):
			row = get_next_open_row_fill(board, col)
			drop_piece(board, row, col, turn)
			pieces += 1
		turn -= 1
		turn += 1
		turn = turn % 2
fill_board(board)
# print_board(board)

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

turn = random.randint(PLAYER, AI)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					# row = get_next_open_row(board, col)
					score = calculate_score(board, get_next_open_row(board, col), col, get_piece(board, col), PLAYER_PIECE)
					add_score(score, PLAYER_PIECE, get_piece(board, col))
					take_piece(board, col, 1)

					# if winning_move(board, PLAYER_PIECE):
					# 	label = myfont.render("Player 1 wins!!", 1, RED)
					# 	screen.blit(label, (40,10))
					# 	game_over = True
					if(is_terminal_node(board)):
						if (PLAYER_1_SCORE > PLAYER_2_SCORE):
							label = myfont.render("Player 1 wins!!", 1, RED)
							screen.blit(label, (40,10))
							game_over = True
						else:
							label = myfont.render("Player 2 wins!!", 1, RED)
							screen.blit(label, (40,10))
							game_over = True

					turn += 1
					turn = turn % 2

					# print_board(board)
					draw_board(board)


	# # Ask for Player 2 Input
	if turn == AI and not game_over:				

		column = random.choice(get_valid_locations(board))
		# print('AI chose to start with column', column)
		# col, score = pick_best_move(board, AI_PIECE)
		col, score = minimax(board, 0, -math.inf, math.inf, True, get_piece(board, column), column)
		# print('max score at:', col, ' score: ', score)
		# if is_valid_location(board, col):
		#pygame.time.wait(500)
		# row = get_next_open_row(board, col)
		add_score(score, AI_PIECE, get_piece(board, col))
		take_piece(board, col, 1)

		# if winning_move(board, AI_PIECE):
		# 	label = myfont.render("Player 2 wins!!", 1, YELLOW)
		# 	screen.blit(label, (40,10))
		# 	game_over = True
		if(is_terminal_node(board)):
			if (PLAYER_1_SCORE > PLAYER_2_SCORE):
				label = myfont.render("Player 1 wins!!", 1, RED)
				screen.blit(label, (40,10))
				game_over = True
			else:
				label = myfont.render("Player 2 wins!!", 1, RED)
				screen.blit(label, (40,10))
				game_over = True

		# print_board(board)
		draw_board(board)

		turn += 1
		turn = turn % 2

	if game_over:
		print('player 1 score: ', PLAYER_1_SCORE, 'player 2 score: ', PLAYER_2_SCORE)
		pygame.time.wait(3000)