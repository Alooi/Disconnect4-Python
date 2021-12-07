import numpy as np
import random
import pygame
import sys
import math
from random import randint
import time
import matplotlib.pyplot as plt

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 10
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

# calculates the score of a certain play defined by the row and column
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

# adds the score to the player specified the piece has to be specified too. 
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

# only used in the fill_board method to initialize the board
def drop_piece(board, row, col, piece):
	board[row][col] = piece

# checks if the the column is not empty
def is_valid_location(board, col):
	# if col == 0:
	# 	print('column zero validation: ', board[0][col] != 0)
	return board[0][col] != 0

# used in the fill_board function, does the opposite of the function above
def is_valid_location_fill(board, col):
	return board[ROW_COUNT-1][col] == 0

# finds the top piece in a row
def get_next_open_row(board, col):
	row = ROW_COUNT-1
	while row >= 0:
		if board[row][col] != 0:
			return row
		row -= 1
	# print('none at column', col)
	# print_board(board)
	return 'dafuq'

# does the opposite of the function above, used in fill_board function only
def get_next_open_row_fill(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

# checks of the board has no more piece to remove
def is_terminal_node(board):
	return len(get_valid_locations(board)) == 0

# removes a piece from the specified column
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

# returns the type of piece at the top of the column specified
def get_piece(board, col):
	row = ROW_COUNT - 1
	while row >= 0:
		if board[row][col] != 0:
			return int(board[row][col])
		row -= 1

# returns an array of none empty columns
def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

# greedy algorithm
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

# called at the start of each run to initialize the board randomly
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
greedywins = 0
minimaxwins = 0
plays = 0
longest_time = 0
average_times = []
n_sizes = []
while plays < 1:
	board = create_board()
	fill_board(board)
	# print_board(board)

	## -- you can ignore this section of the code --
	pygame.init()

	SQUARESIZE = 50

	width = COLUMN_COUNT * SQUARESIZE
	height = (ROW_COUNT+1) * SQUARESIZE

	size = (width, height)

	RADIUS = int(SQUARESIZE/2 - 5)

	screen = pygame.display.set_mode(size)
	draw_board(board)
	pygame.display.update()

	myfont = pygame.font.SysFont("monospace", 75)

	turn = random.randint(PLAYER, AI)
	game_over = False
	PLAYER_1_SCORE = 0
	PLAYER_2_SCORE = 0
	time_list = []
	
	

## --------------------------------------------

	while not game_over:

		if turn == PLAYER and not game_over:				

			col = random.choice(get_valid_locations(board)) # random choice
			# print('AI chose to start with column', column)
			# col, score = pick_best_move(board, AI_PIECE)  # greedy
			# col, score = minimax(board, 0, -math.inf, math.inf, True, get_piece(board, column), column) # minimix
			# print('max score at:', col, ' score: ', score)
			# if is_valid_location(board, col):
			#pygame.time.wait(500)
			# row = get_next_open_row(board, col)
			score = calculate_score(board, get_next_open_row(board, col), col, get_piece(board, col), PLAYER_PIECE)
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
					greedywins += 1
					game_over = True
				else:
					label = myfont.render("Player 2 wins!!", 1, RED)
					screen.blit(label, (40,10))
					minimaxwins += 1
					game_over = True

			# print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2
		# # Ask for Player 2 Input
		elif turn == AI and not game_over:				

			
			# start_time = time.time()
			# col, score = pick_best_move(board, AI_PIECE) # greedy
			# time_taken = time.time() - start_time
			# if time_taken: time_list.append(time_taken)

			column = random.choice(get_valid_locations(board))
			start_time = time.time()
			col, score = minimax(board, 0, -math.inf, math.inf, True, get_piece(board, column), column) # minimix
			time_taken = time.time() - start_time
			if time_taken: time_list.append(time_taken)

			if time_taken > longest_time:
				longest_time = time_taken
				if average_times:
					if 1000*longest_time > average_times[len(average_times)-1]:
						print('found a longer one')
						game_over = True
			# time_list.append(time_taken)
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
					greedywins += 1
					game_over = True
				else:
					label = myfont.render("Player 2 wins!!", 1, RED)
					screen.blit(label, (40,10))
					minimaxwins += 1
					game_over = True

			# print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

		# if game_over:
			# print('greedy score: ', PLAYER_1_SCORE, 'minimax score: ', PLAYER_2_SCORE)
			# pygame.time.wait(3000)
	plays += 1
	# if longest_time:
	# 	if not average_times:
	# 		average_times.append(1000*longest_time)
	# 		n_sizes.append(COLUMN_COUNT)
	# 		longest_time = 0
	# 	elif 1000*longest_time > average_times[len(average_times)-1]:
	# 		average_times.append(1000*longest_time)
	# 		n_sizes.append(COLUMN_COUNT)
	# 		longest_time = 0
	if longest_time:
		average_times.append(1000*longest_time)
		n_sizes.append(COLUMN_COUNT)
		longest_time = 0
	COLUMN_COUNT = COLUMN_COUNT*2
	# n_sizes.append(ROW_COUNT)
	# ROW_COUNT = ROW_COUNT+1
	# summation = 0
	# for c in range(len(time_list)):
	# 	summation += time_list[c]
# print('greedy vs minimax: ', greedywins, '|', minimaxwins)
# print('time taken for each move: ')
# print(time_list)
print('longest time: ', time_list)
num_plays = []
c = 0
while c < len(time_list):
	num_plays.append(c+1)
	c += 1

plt.plot(num_plays, time_list, 'b')
plt.xlabel('turn number')
plt.ylabel('time (ms)')
plt.title('Time vs turn number Graph')
plt.show()