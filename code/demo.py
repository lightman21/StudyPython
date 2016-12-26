class A(object):
	a = 'sdf'
	b = 'fasd'

	def __init__(self, c):
		self.c = c


	def set_c(self, c):
		self.c = c

	@classmethod
	def set_b(cls, b):
		cls.b = b

	@staticmethod
	def hello(h):
		print(h)

	def hello2(h):
		print(h)
