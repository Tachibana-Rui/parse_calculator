import io
import tokenize


class TokenizeWrapper:
	def __init__(self, line):
		self.line = line
		self.tokens = tokenize.generate_tokens(io.StringIO(line).readline)
		self.current = next(self.tokens)
		self.previous = 'START'

	def __str__(self):
		return self.current[1]

	def get_current(self):
		if self.current[0] > 0:
			return self.current[1]
		else:
			return 'NO MORE TOKENS'

	def get_previous(self):
		return self.previous

	def next(self):
		# The return value is mainly intended for debugging purposes
		if self.has_next():
			self.previous = self.current[1]
			self.current = next(self.tokens)
			return self.current
		else:
			return (0, 'EOS')

	def is_number(self):
		return self.current[0] == 2

	def is_name(self):
		return self.current[0] == 1

	def is_newline(self):
		return self.current[0] == 4

	def is_at_end(self):
		return self.current[0] == 0 or self.current[0] == 4

	def has_next(self):
		return self.current[0] != 0 and self.current[0] != 4

	def replace(self,replacer):
		self.line=self.line[:self.current.start[1]]+str(replacer)+self.line[self.current.end[1]:]
		return self.line

def main():
	line1 = 'hello! 123.4 (1e10 ++) - LAST '
	line2 = '(4+4)/(-2*2)'
	line3 = '1+*2'
	w = TokenizeWrapper(line2)
	
	try:
		while w.has_next():
			print(w.get_current(), end='\t')
			if w.is_name():
				print('NAME')
			elif w.is_number():
				print('NUMBER')
			else:
				print()
			w.next()
	except tokenize.TokenError:  # For handling unbalanced parentheses
		print('*** Unbalanced parentheses')
	for i in w.tokens:
		print(i)
	print('Bye')


if __name__ == '__main__':
	main()
