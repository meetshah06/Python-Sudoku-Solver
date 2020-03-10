import time

board = [
[1, 0, 0, 0, 4, 0, 0, 0, 0],
[0, 9, 2, 6, 0, 0, 3, 0, 0],
[3, 0, 0, 0, 0, 5, 1, 0, 0],
[0, 7, 0, 1, 0, 0, 0, 0, 4],
[0, 0, 4, 0, 5, 0, 6, 0, 0],
[2, 0, 0, 0, 0, 4, 0, 8, 0],
[0, 0, 9, 4, 0, 0, 0, 0, 1],
[0, 0, 8, 0, 0, 6, 5, 2, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 6]
]

# board = [
#     [7,8,0,4,0,0,1,2,0],
#     [6,0,0,0,7,5,0,0,9],
#     [0,0,0,6,0,1,0,7,8],
#     [0,0,7,0,4,0,2,6,0],
#     [0,0,1,0,5,0,9,3,0],
#     [9,0,4,0,6,0,0,0,5],
#     [0,7,0,3,0,0,0,1,2],
#     [1,2,0,0,0,7,4,0,0],
#     [0,4,9,2,0,6,0,0,7]
# ]


def solve(bo):

	find = find_empty(bo)

	# If no empty position found
	if not find:
		# Then solution found
		return True
	else:
		row, col = find
		# print(row, col)

	# Generate numbers from 1-9 to insert
	for i in range(1, 10):
		# If insertion is valid
		if valid(bo, i, (row, col)):
			# Insert the number in the board
			bo[row][col] = i
			# print(bo)

			# Attempt to solve again with the new value inserted
			if solve(bo):
				return True

			# If anywhere solution is not possible, the algorithm returns False and return here
			# We then revert the last change we made
			bo[row][col] = 0

	# If no number can be inserted, solution is wrong and backtrack
	return False


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

def print_board(bo):
	# Iterate through all rows
	for i in range(len(bo)):
		# Print a '----' after every 3 rows
		if i%3 == 0 and i!=0:
			print("------------------------")
		for j in range(len(bo[0])):
			# Print a '|' after every 3 numbers
			if j%3==0 and j!=0:
				print(" | ", end="")
			# If last number in row, print and new line	
			if j==8:
				print(bo[i][j])
			else:
				print(str(bo[i][j]) + " ", end="")


# Find the empty blocks
def find_empty(bo):
	# print("in empty")
	for i in range(len(bo)):
		for j in range(len(bo)):
			# 0 means empty
			if bo[i][j] == 0:
				# Return row, col
				# print(i, j)
				return (i, j)
	return None


print_board(board)
start = time.time()
solve(board)
end = time.time()
print()
print("Solved :-")
print_board(board)
print()
print("Time taken =", end-start)

# print(len(board))
# print(len(board[0]))