import io
import math
from tokenize import TokenError
from tokenizer import TokenizeWrapper

#DEFINES
cdict = {'PI':3.141592653589793,'E':2.718281828459045,'ans':0.0}
predefined_namelist=('PI','E','ans','sin','cos','tan','asin','acos','atan','log','ln','exp')
function_namelist=('sin','cos','tan','asin','acos','atan','log','ln','exp')

class CalculatorException(Exception):
	def __init__(self,desc):
		self.desc = desc

def	assignment(wtok):
	result = expression(wtok)
	while wtok.has_next():
		if wtok.get_current() == '=':
			wtok.next()
			t= wtok.get_current()
			if wtok.is_name() and (t not in predefined_namelist):
				cdict[t]=result
			else:
				raise CalculatorException(f"***Error. Expected a variable name after '=' but found '{wtok.get_current()}'")
		elif wtok.get_previous()!='=':
			break
		else:
			wtok.next()
	return result


def expression(wtok):
	result = term(wtok)
	while wtok.get_current() == '+':
		wtok.next()	
		result = result + term(wtok)
	while wtok.get_current() == '-':
		wtok.next()	
		result = result - term(wtok)
	return result


def term(wtok):
	result = factor(wtok)
	while wtok.get_current() == '*':
		wtok.next()
		if wtok.get_current() == '/':
			raise CalculatorException('***Error. Expected number, name or ’(’')
		else:
			result = result * factor(wtok)
	while wtok.get_current() == '/':
		wtok.next()
		if wtok.get_current() == '*' :
			raise CalculatorException('***Error. Expected number, name or ’(’')
		else:
			try:
				result = result / factor(wtok)
			except:
				raise CalculatorException('***Error. Divided by zero')
	return result


def factor(wtok):
	if wtok.get_current() == '(' :
		wtok.next()				  # bypass (
		result = assignment(wtok)
		wtok.next()				  # bypass )
	elif wtok.is_number():
		result = float(wtok.get_current())
		wtok.next()
	elif wtok.is_name():
		result=function_name(wtok)
	elif wtok.get_current() == '-' :
		wtok.next()
		result = 0 - factor(wtok)
	else:
		raise CalculatorException(f"***Error. Expected a left parentheses or number but found '{wtok.get_current()}'")
	return result


def function_name(wtok):
	fn=wtok.get_current()
	if fn not in function_namelist and fn!='vars':
		try:
			wtok.next()
			return cdict[fn]
		except:
			raise CalculatorException('***Error. Invalid syntax or using undefined variables')
	else:
		try:
			if fn in ['sin','cos','tan','asin','acos','atan','exp']:
				wtok.next()
				a='math.'+fn+wtok.get_current()+str(assignment(wtok))+')'
				return eval(a)
			elif fn == 'log':
				wtok.next()
				a='math.log'+wtok.get_current()+str(assignment(wtok))+',10)'
				return eval(a)
			elif fn == 'ln':
				wtok.next()
				a='math.log'+wtok.get_current()+str(assignment(wtok))+')'
				return eval(a)
		except ValueError:
			raise CalculatorException(f"***Error. Mathematical function '{fn}' out of range")
		except :
			raise CalculatorException(f"***Error. Expected a left parentheses after '{fn}'")

def statement(wtok):
	global cdict
	if wtok.get_current() == 'quit':
		wtok.next()
		if wtok.get_current()!='':
			raise CalculatorException('***Error. There are more stuff on the line')
		else:
			print('Bye!')
			exit()
	elif wtok.get_current() == 'vars':
		print(cdict)
		wtok.next()
	elif wtok.get_current() == 'reset':
		cdict.clear()
		cdict = {'PI':3.141592653589793,'E':2.718281828459045,'ans':0.0}
		wtok.next()
	while wtok.get_current() != '':
		return assignment(wtok)

def print_result():
	if cdict['ans']!=None:
		print('Result: ', cdict['ans'])
	else:
		print('Success')
	if len(cdict)>3:
		for a,b in cdict.items():
			if a not in predefined_namelist:
				print(a,'=',b)

def main():
	print("Very simple calculator")
	b=True
	while True:
		line = input('> ')
		try:
			if line.find('**')==-1 and line.find('//')==-1:
				wtok = TokenizeWrapper(line)
				cdict['ans'] = statement(wtok)
				print_result()
			else:
				raise CalculatorException("***Error. Unsupported operator '**' or '//'")
		except TokenError:
			print('*** Error. Unbalanced parentheses')
		except CalculatorException as e:
			print(e)




if __name__ == "__main__":
	main()
