import pygame
import time
pygame.font.init()

class Grid:
	# board = [
	# [1, 0, 0, 0, 4, 0, 0, 0, 0],
	# [0, 9, 2, 6, 0, 0, 3, 0, 0],
	# [3, 0, 0, 0, 0, 5, 1, 0, 0],
	# [0, 7, 0, 1, 0, 0, 0, 0, 4],
	# [0, 0, 4, 0, 5, 0, 6, 0, 0],
	# [2, 0, 0, 0, 0, 4, 0, 8, 0],
	# [0, 0, 9, 4, 0, 0, 0, 0, 1],
	# [0, 0, 8, 0, 0, 6, 5, 2, 0],
	# [0, 0, 0, 0, 1, 0, 0, 0, 6]
	# ]

	board = [
	    [7,8,0,4,0,0,1,2,0],
	    [6,0,0,0,7,5,0,0,9],
	    [0,0,0,6,0,1,0,7,8],
	    [0,0,7,0,4,0,2,6,0],
	    [0,0,1,0,5,0,9,3,0],
	    [9,0,4,0,6,0,0,0,5],
	    [0,7,0,3,0,0,0,1,2],
	    [1,2,0,0,0,7,4,0,0],
	    [0,4,9,2,0,6,0,0,7]
	]

	def __init__(self, rows, cols, width, height, win):
		self.rows = rows
		self.cols = cols
		self.width = width
		self.height = height
		self.win = win
		# Create a cube object for every every cube in the grid
		self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
		# Model of board needed to pass to solve function
		self.model = None
		self.update_model()
		# To store (row, col) of cube that is selected
		self.selected = None
		

	# Set the model equal to current state of sudoku
	def update_model(self):
		self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

	# Put the value in the selected cube
	def place(self, val):
		# Get the cube which is selected
		row, col = self.selected
		# If it is initially empty
		if(self.cubes[row][col].value == 0):
			# Set the value
			self.cubes[row][col].set(val)
			self.update_model()

			# If the value inserted is valid then return true
			if valid(self.model, val, (row, col)) and self.solve():
				return True

			# Else reset the value to 0 and return false
			else:
				self.cubes[row][col].set(0)
				self.cubes[row][col].set_temp(0)
				self.update_model()
				return False

	# Put the pencil value
	def sketch(self, val):
		row, col = self.selected
		self.cubes[row][col].set_temp(val)

	# Draw the board
	def draw(self):
		# Draw Grid Lines
		gap = self.width / 9
		# For 9 rows or columns 10 lines are required; hence self.rows+1
		for i in range(self.rows+1):
			if i % 3 == 0 and i != 0:
				thick = 4
			else:
				thick = 1
			# Horizontal Lines
			pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
			# Vertical Lines
			pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

		# Draw Cubes
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].draw(self.win)


	# Select a particular Cube
	def select(self, row, col):
		# Reset all other cubes
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].selected = False

		self.cubes[row][col].selected = True
		self.selected = (row, col)

	# Remove any pencil mark
	def clear(self):
		row, col = self.selected
		# If no permanent value is set i.e cube is empty
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set_temp(0)


	# Get the position of cube which is clicked
	def click(self, pos):
		# If clicl is within the window size
		if pos[0] < self.width and pos[1] < self.height:
			gap = self.width / 9
			x = pos[0] // gap
			y = pos[1] // gap
			# y gives the row and x gives the column
			return (int(y), int(x))
		else:
			return None

	# If sudoku is solved
	def is_finished(self):
		for i in range(self.rows):
			for j in range(self.cols):
				if self.cubes[i][j].value == 0:
					return False
		return True


	# Actual Backtracking Algorithm
	def solve(self):
		find = find_empty(self.model)
		if not find:
			return True
		else:
			row, col = find

		for i in range(1, 10):
			if valid(self.model, i, (row, col)):
				self.model[row][col] = i

				if self.solve():
					return True

				self.model[row][col] = 0

		return False


	def solve_gui(self):
		find = find_empty(self.model)
		if not find:
			return True
		else:
			row, col = find

		for i in range(1, 10):
			if valid(self.model, i, (row, col)):
				self.model[row][col] = i
				self.cubes[row][col].set(i)
				# Highlight the cube with green
				self.cubes[row][col].draw_change(self.win, True)
				self.update_model()
				pygame.display.update()
				pygame.time.delay(100)

				if self.solve_gui():
					return True

				self.model[row][col] = 0
				self.cubes[row][col].set(0)
				self.update_model()
				# Highlight the cube with red
				self.cubes[row][col].draw_change(self.win, False)
				pygame.display.update()
				pygame.time.delay(100)

		return False


class Cube:
	rows = 9
	cols = 9

	def __init__(self, value, row, col, width, height):
		self.value = value
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		# To denote if a cube has been selected
		self.selected = False
		# To store the pencil value to be drawn
		self.temp = 0


	# Put the text into the cube
	def draw(self, win):
		fnt = pygame.font.SysFont("comicsans", 40)

		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		# Draw the pencil value
		if self.temp != 0 and self.value == 0:
			text = fnt.render(str(self.temp), 1, (128, 128, 128))
			win.blit(text, (x+5, y+5))

		# Draw the fixed value 
		elif not (self.value == 0):
			text = fnt.render(str(self.value), 1, (0, 0, 0))
			win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

		# Draw a rectangle to show that cube is selected
		if self.selected:
			pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)


	# For solve_gui()
	def draw_change(self, win, g=True):
		fnt = pygame.font.SysFont("comicsans", 40)

		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		# Make rectangle white first so that colours do not overlap
		pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

		text = fnt.render(str(self.value), 1, (0, 0, 0))
		win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

		if g:
			pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
		else:
			pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)


	# Set fixed value
	def set(self, val):
		self.value = val

	# Set pencil mark value
	def set_temp(self, val):
		self.temp = val


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


# Check if insertion of num at empty position pos is allowed
def valid(bo, num, pos):

	# Check row
	for i in range(len(bo)):
		# num already present in the row; do not check in the same position we have just inserted
		if(bo[pos[0]][i] == num and pos[1] != i):
			return False

	# Check column
	for i in range(len(bo)):
		# num already present in the column; do not check in the same position we have just inserted
		if(bo[i][pos[1]] == num and pos[0] != i):
			return False

	# Get the 3x3 box coordinates
	# (0,0) will be the first 3x3 box; (0,1) the second and so on
	box_x = pos[1] // 3 # pos[1] is for column value which is vertical
	box_y = pos[0] // 3 # pos[0] is row value which is horizontal
	
	# Check in the box
	for i in range(box_y*3, box_y*3 + 3):
		for j in range(box_x*3, box_x*3 + 3):
			# If num already present; do not check in the same position we have already inserted
			if(bo[i][j] == num and (i, j) != pos):
				return False

	# It is valid
	return True


def redraw_window(win, board, time, strikes):
	# Fill the background with white colour
	win.fill((255, 255, 255))
	# Draw Time
	fnt = pygame.font.SysFont("comicsans", 40)
	text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
	win.blit(text, (540 - 160, 560))
	# Draw strikes
	text = fnt.render("X " * strikes, 1, (255, 0, 0))
	win.blit(text, (20, 560))
	# Draw grid and board
	board.draw()

def format_time(secs):
	sec = secs % 60
	minute = secs // 60
	hour = minute // 60

	time = " " + str(minute) + ":" + str(sec)
	return time


def main():
	# Set the window size
	win = pygame.display.set_mode((540, 600))
	pygame.display.set_caption("Soduko")
	board = Grid(9, 9, 540, 540, win)
	# Store the key pressed
	key = None
	run = True
	start = time.time()
	# Calc the number of wrong answers
	strikes = 0

	while(run):
		play_time = round(time.time() - start)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:				
				if event.key == pygame.K_1:
					key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9
				if event.key == pygame.K_DELETE:
					# Delete the pencil mark value
					board.clear()
					key = None


				if event.key == pygame.K_SPACE:
					board.solve_gui()
					# run = False

				if event.key == pygame.K_RETURN:
					i, j = board.selected
					# If value is entered
					if board.cubes[i][j].temp != 0:
						# If value is valid
						if board.place(board.cubes[i][j].temp):
							print("Success")
						else:
							print("Wrong")
							strikes += 1
						key = None

						# After successfully putting a value check if sudoku completed
						if board.is_finished():
							print("Game Over")

			if event.type == pygame.MOUSEBUTTONDOWN:
				# Get the mouse click position
				pos = pygame.mouse.get_pos()
				# print(pos)
				# Get the cube position
				clicked = board.click(pos)
				if clicked:
					# Highlight the cube
					board.select(clicked[0], clicked[1])
					key = None

			# Write the pencil value
			if board.selected and key != None:
				board.sketch(key)

		redraw_window(win, board, play_time, strikes)
		pygame.display.update()

main()
pygame.quit()