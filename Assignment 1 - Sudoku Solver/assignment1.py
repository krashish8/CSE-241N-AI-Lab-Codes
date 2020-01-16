def read_matrix(filename):
	with open(filename, "r") as f:
		matrix = f.readlines()
		for i,row in enumerate(matrix):
			matrix[i] = list(map(int,matrix[i].split(",")))
	return matrix

def write_matrix(filename, solved_matrix):
	with open(filename, "w") as f:
		f.writelines(','.join(str(j) for j in i) + '\n' for i in solved_matrix)
	print(filename+" for backtracking generated.")

class sudoku():
	def __init__(self, filename):
		self.matrix = read_matrix(filename)		

	def solve(self, row_no=0, col_no=0):
		# Initializing some values
		if row_no == 0 and col_no == 0:
			self.is_occupied_row = [[0 for _ in range(10)] for _ in range(9)]
			self.is_occupied_column = [[0 for _ in range(10)] for _ in range(9)]
			self.is_occupied_box = [[0 for _ in range(10)] for _ in range(9)]

			for rowno in range(9):
				for colno in range(9):
					val = self.matrix[rowno][colno]
					if val:
						boxno = rowno//3 + colno//3*3
						self.is_occupied_row[rowno][val] = 1
						self.is_occupied_column[colno][val] = 1
						self.is_occupied_box[boxno][val] = 1
		if col_no == 9:
			row_no += 1
			col_no = 0
		if row_no == 9:
			return 1
		else:
			if self.matrix[row_no][col_no]:
				if self.solve(row_no, col_no + 1):
					return 1
			else:
				for val in range(1, 10):
					box_no = row_no//3 + col_no//3*3
					if self.is_occupied_row[row_no][val] or self.is_occupied_column[col_no][val] or self.is_occupied_box[box_no][val]:
						continue
					self.matrix[row_no][col_no] = val
					self.is_occupied_row[row_no][val] = 1
					self.is_occupied_column[col_no][val] = 1
					self.is_occupied_box[box_no][val] = 1

					if self.solve(row_no, col_no + 1):
						return 1

					self.matrix[row_no][col_no] = 0
					self.is_occupied_row[row_no][val] = 0
					self.is_occupied_column[col_no][val] = 0
					self.is_occupied_box[box_no][val] = 0

	def solve_without_backtracking(self):
		self.occupied_values = lambda row_no, col_no : {self.matrix[i][j] for i in range(9) for j in range(9) if i == row_no or j == col_no or i//3 + j//3*3 == row_no//3 + col_no//3*3}
		L = [(len(self.occupied_values(i, j)),self.occupied_values(i,j),i,j) for i in range(9) for j in range(9) if self.matrix[i][j] == 0]
		if not L:
			return 1
		_, occupied_val_set, row_no, col_no = max(L)
		for i in {1,2,3,4,5,6,7,8,9} - occupied_val_set:
			self.matrix[row_no][col_no]=i
			if self.solve_without_backtracking():
				return 1
		self.matrix[row_no][col_no] = 0
		return 0
		raise NotImplementedError("You need to fill the non-backtracking function") 

if __name__=="__main__":
	su = sudoku("data.txt")
	su.solve()
	write_matrix("sol.txt", su.matrix)
	try:
		su = sudoku("data.txt")
		su.solve_without_backtracking()
		print("Solved sudoku matrix without backtracking:")
		for i in range(9):
			print(*su.matrix[i], sep=" ")
	except Exception as e:
		print(e)



