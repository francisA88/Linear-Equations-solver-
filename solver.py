#Programmed in Python 3.7 but with a few adjustments, can be run in other versions of Python 3
#The code does not do any rearrangememt or collection of like terms, so that has to be done yourself
import numpy as np
from copy import deepcopy
import re
import string

UCASE = string.ascii_lowercase
LCASE = string.ascii_uppercase

class VariableError(Exception): pass

class EqnSolver(object):
	def __init__(self, eqns:list, constants:list):
		self.eqns = eqns
		self.varCount = len(constants)
		self.constants = constants
	
	def solve(self):
		try:
			result = []
			bigDet = np.matrix(self.eqns)
			bigDet = np.linalg.det(bigDet)
			def getdet(n=0):
				m = deepcopy(self.eqns)
				for i in range(self.varCount):
					m[i][n] = self.constants[i]
				return np.linalg.det(np.matrix(m))
				
			for i in range(self.varCount):
				d = getdet(i)
				result.append(round(d/bigDet, 5))
			return result
		except Exception as error:
			if type(error) == np.linalg.LinAlgError:
				return "Number of equations must be equal to the number of variables."
			else:
				return "Error!"


def split(expr) -> list:
	#First of all, i should get rid of whitespaces for convenience sake
	expr = expr.replace(" ", "")
	varPart = re.findall("[+-]*[0-9]*\.?[0-9]*[A-Za-z]", expr)
	if re.search("[A-Za-z][A-Za-z]", expr):
		return "Variable cluster found. Variables must be single"
	if re.search("\.\.", expr):
		return "Error, please remove double points"
	temp = expr
	for p in varPart:
		temp = temp.replace(p, "")
	temp = temp.replace("=","")
	eqindex = expr.index("=") if "=" in expr else 0
	constant = eval(temp) if expr.index(temp) > eqindex else -eval(temp)
	eqn = []
	variables = sorted([i for i in expr if i.isalpha()])
	for i in variables:
		for j in varPart:
			if i in j:
				coeff = j[:-1]
				if coeff == "":
					#If the constant comes before the equals sign, use -1 instead. This is because it changes sign when crossing over the equals sign
					coeff = coeff+"1"
					if expr.index(j) < eqindex: eqn.append(eval(coeff))
					else: eqn.append(-eval(coeff))
				elif re.fullmatch("[+-]+", coeff):
					coeff = coeff + "1"
					if expr.index(j) < eqindex: eqn.append(eval(coeff))
					else: eqn.append(-eval(coeff))
				else:
					if expr.index(j) < eqindex: eqn.append(eval(coeff))
					else: eqn.append(-eval(coeff))
	eqn.append(constant)
	return eqn
	
	

if __name__ == "__main__":
	m = [
		[1, 1, 1],
		[3, 1, -4],
		[1, 2, -1]
		]
	s = EqnSolver(eqns=m, constants=[6, -7, 2])
#	print(s.solve())
	eqns = [
		"a+b+c-2d+w-x + y +z= 6",
		"a-b+3c-2d-4w+x + y -z = 12",
		"3a+2b-5c+4d-w+x - y +z= 14",
		"5a-2w-6d+14b-66c+x -y -z = 81",
		"5a-2w-6d+44b-66c+x -y -z = 41",
		"5a-2w-6d+14b-16c+x -y -z = 27",
		"5a-12w-6d+14b-66c+x -y -z = 21",
		"7a-2w-6d+14b-66c+x -y -5z = 98",
		"7a-2w-6d+14b-66c+x -22y-5z = 21",
		"7a-2w-6d+18b-66c+x -y -5z = 27"
	]
	vars = [split(i)[:-1] for i in eqns]
	c = [split(i)[-1] for i in eqns]
	print(EqnSolver(vars, c).solve())