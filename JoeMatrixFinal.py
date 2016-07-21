"""
Joe's Matrix tool.

This program performs various operations on matrices specified by the user. 
It then outputs the result of each operation to the user and allows
the user to take that output into further operations continuously.

Although the python "numpy" module can perform some matrix algebra, I have written
this program using mostly pure python code as a personal challenge.

Written with Python 2.7
"""
from fractions import Fraction

def start():
	print "\nWelcome to Joe's Matrix tool \n\nWhere would you like to start? \
	\n\n1. Matrix Addition \n2. Matrix Multiplication \n3. Find a determinant \
	\n4. Find a transpose \n5. Find an inverse"

	while True:
		operation = int(raw_input("\nEnter your selection (1-5):"))
		if 1 > operation or 5 < operation:
			print "Selection must be between 1 and 5"
 		else:
			break
	stage_one(operation)


class Matrix(object):

	"""A Class of blank matrices of given size, with methods to print the matrix, change the elements by user input, 
	find the transpose, find the determinant and find the inverse.
	"""

	def __init__(self,rows,columns):
		self.rows = rows
		self.columns= columns
		self.matrix = [[int(0) for x in range(self.columns)] for x in range(self.rows)]

	def __len__(self):
		return len(self.matrix)

	def print_m(self):
		for line in self.matrix:
			print line

	def input_matrix(self):
		for r in range(self.rows):
			while True:
				matinput = (raw_input('Enter Row {b} with length {a}: '.format(b = r+1, a = self.columns))).strip()
				try:
					row = [int(x) for x in matinput.split(' ')]
				except:
					print 'There was an error inputting numbers, retry'
					continue
				if len(row) != self.columns:
					print 'You must enter the correct number of values...'
					continue
				else:
					break
			self.matrix[r] = row
		self.print_m()

	def transpose(self):
		tran_m = Matrix(self.columns,self.rows)
		tran_m.matrix = [[row[i] for row in self.matrix] for i in range(self.columns)]
		return tran_m

	def determinant(self,mat):
		
		# The determinant is found by a recursive algorithm which applies the Laplace expansion

		if mat.rows == 2 and mat.columns == 2:
			return mat.matrix[0][0] * mat.matrix[1][1] - mat.matrix[0][1] * mat.matrix[1][0]
			
		det = 0
		plus = True
		
		for i in range(mat.columns):
			sub = self.sub_matrix(mat,0,i)
			if plus == True:
				det += mat.matrix[0][i] * self.determinant(sub)
			else:
				det -= mat.matrix[0][i] * self.determinant(sub)

			plus = not plus
		return det

	def invert(self):
		"""
		The inverse of a matrix is found via the matrix of cofactors (which is found using the determinant method above).
		The inverse is printed to the user displaying the elements as fractional approximations, but the floating point values
		are returned to the program for further use.
		"""
		det = self.determinant(self)
		if det == 0:
			print "\nThis matrix is not invertible. Determinant is zero."
			return self
		else:
			cofactors = Matrix(self.rows,self.columns)
			plus = True
			for i in range(self.columns):
				for j in range(self.rows):
					sub = self.sub_matrix(self,i,j)
					minor = sub.determinant(sub)
					if plus == True:
						cofactors.matrix[i][j] = minor	
					else:
						cofactors.matrix[i][j] = -1 * minor
					plus = not plus
				plus = not plus
			inverse = cofactors.transpose()
			for i in range(inverse.columns):
				for j in range(inverse.rows):
					inverse.matrix[i][j] = inverse.matrix[i][j] / float(det)
			
			frac_inv = Matrix(self.rows,self.columns)
			for i in range(frac_inv.columns):
				for j in range(frac_inv.rows):
					frac_inv.matrix[i][j] = str(Fraction(inverse.matrix[i][j]).limit_denominator(999))
			print "\nThe inverse of the matrix is:"
			frac_inv.print_m()
			
			return inverse
		
	def sub_matrix(self,n_matrix,row,col):
		"""
		This method is used by the determinant and invert methods to find the required
		(n-1) x (n-1) matrices in the calculations.
		"""
		nmin1_matrix = Matrix(n_matrix.rows-1, n_matrix.columns-1)

		c = 0
		for i in range(n_matrix.rows):
			for j in range(n_matrix.columns):
				if i == row or j == col:
					continue
				x = c / nmin1_matrix.columns
				y = c % nmin1_matrix.rows
				nmin1_matrix.matrix[x][y] = n_matrix.matrix[i][j]
				c += 1
		return nmin1_matrix


def create_blank(multiply, mat):

	#User Input Driven Blank Matrix Creation"""

	if multiply == False:
		mrows = int(raw_input('How Many Rows?  '))
	else:
		mrows = mat.columns
	mcolumns = int(raw_input('How Many Columns?  '))
	return Matrix(mrows,mcolumns)
	

def addition(m1, m2):

	# Addition function
	global output_m
	output_m = Matrix(m1.rows,m1.columns)
	for i in range(m1.rows):
		for j in range(m1.columns):
			output_m.matrix[i][j] = m1.matrix[i][j] + m2.matrix[i][j]
	print "\nMatrix 1 + Matrix 2 gives:"
	output_m.print_m()
	stage_two(output_m)


def multiplication(m1, m2):

	#multiplication function
	global output_m
	output_m = Matrix(m1.rows,m2.columns)
	for i in range(m1.rows):
		for j in range(m2.columns):
			for k in range(m2.rows):
				output_m.matrix[i][j] += m1.matrix[i][k] * m2.matrix[k][j]
	print "\nMatrix 1 * Matrix 2 gives:"
	output_m.print_m()
	stage_two(output_m)


def stage_one(operation):

	if operation == 1 or operation == 2 or operation == 4:
		print "\nPlease enter the first matrix"
		user_m1 = create_blank(False,None)
		user_m1.input_matrix()
		if operation == 4:
			tran = user_m1.transpose()
			print "\nThetranspose is:\n"
			tran.print_m()
			stage_two(tran)
		else:
			print "\nPlease enter the second matrix"
			if operation == 1:
				user_m2 = Matrix(user_m1.rows,user_m1.columns)
				user_m2.input_matrix()
				addition(user_m1, user_m2)	
			else:
				user_m2 = create_blank(True,user_m1)
				user_m2.input_matrix()
				multiplication(user_m1, user_m2)
		
	if operation == 3 or operation == 5:
		order = int(raw_input("\nHow many rows in the square matrix?"))
		user_m1 = Matrix(order,order)
		user_m1.input_matrix()
		if operation == 3:
			print "\nThe determinant is %s" % (user_m1.determinant(user_m1))
			stage_two(user_m1)
		else:
			output_m = user_m1.invert()
			stage_two(output_m)

def stage_two(reuse_m):
	while True:
		more = str(raw_input("\nDo something else? Y/N:"))
		more = more.upper()
		if more == "Y":
			stage_three(reuse_m)
		elif more == "N":
			print "\nGoodbye"
			break
		else:
			print "Enter Y or N"
			continue

def stage_three(reuse_m):
	print "\nWhat's next? \n1. Find the determinant \n2. Transpose this matrix \
	\n3. Invert this matrix \n4. Reuse in addition \n5. Reuse in multiplication \
	\n6. Start over again"
	
	while True:
		choice = int(raw_input("\nEnter your selection (1-6):"))
		if 1 > choice or 6 < choice: 
			print "Selection must be between 1 and 6"
 		else:
			break
	if choice == 1:
		if reuse_m.rows == reuse_m.columns:	
			print "\nThe determinant is %s" % (reuse_m.determinant(reuse_m))
		else:
			print "\nThis matrix is not square. The determinant is undefined"
		stage_two(reuse_m)
	if choice == 2:
		tran = reuse_m.transpose()
		print "\nThetranspose is:\n"
		tran.print_m()
		stage_two(tran)
	if choice == 3:
		if reuse_m.rows == reuse_m.columns:
			output_m = reuse_m.invert()
			stage_two(output_m)
		else:
			print "\nThis matrix is not square. Cannot find inverse."
	if choice == 4:
		user_m2 = Matrix(reuse_m.rows,reuse_m.columns)
		user_m2.input_matrix()
		addition(reuse_m, user_m2)
	if choice == 5:
		user_m2 = create_blank(True,reuse_m)
		user_m2.input_matrix()
		multiplication(reuse_m, user_m2)
	if choice == 6:
		start()
	
	
start()


	

		


	
		






	


