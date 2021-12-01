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
	add_score(max_k, player, piece)
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
	print('player1 total score: ', PLAYER_1_SCORE)
	print('player2 total score: ', PLAYER_2_SCORE)


def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[0][col] != 0

def get_next_open_row(board, col):
	row = ROW_COUNT
	while row >= 0:
		if board[row][col] != 0:
			return row
	row -= 1

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return len(get_valid_locations(board)) == 0

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

def minimax(board, depth, alpha, beta, maximizingPlayer, piece, column):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if maximizingPlayer:
		player = 2
	else:
		player = 1
	if depth < ROW_COUNT or is_terminal:
		return (None, calculate_score(board, get_piece(board, column), column, piece, player))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			# row = get_next_open_row(board, col)
			b_copy = board.copy()
			take_piece(b_copy,col,player)
			new_score = minimax(b_copy, depth+1, alpha, beta, False, piece, column)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		print('maxinmizing score:', column, value)
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			# row = get_next_open_row(board, col)
			b_copy = board.copy()
			take_piece(b_copy,col,player)
			new_score = minimax(b_copy, depth+1, alpha, beta, True, piece, column)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		print('minimizing score:', column, value)
		return column, value

def get_piece(board, col):
	row = ROW_COUNT
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

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

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
print_board(board)
game_over = False
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
					take_piece(board, col, 1)

					# if winning_move(board, PLAYER_PIECE):
					# 	label = myfont.render("Player 1 wins!!", 1, RED)
					# 	screen.blit(label, (40,10))
					# 	game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)


	# # Ask for Player 2 Input
	if turn == AI and not game_over:				

		column = random.randint(0, COLUMN_COUNT-1)
		#col = pick_best_move(board, AI_PIECE)
		col, minimax_score = minimax(board, 0, -math.inf, math.inf, True, get_piece(board, column), column)

		if is_valid_location(board, col):
			#pygame.time.wait(500)
			# row = get_next_open_row(board, col)
			take_piece(board, col, 1)

			# if winning_move(board, AI_PIECE):
			# 	label = myfont.render("Player 2 wins!!", 1, YELLOW)
			# 	screen.blit(label, (40,10))
			# 	game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)