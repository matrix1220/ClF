from new_try import *
evals = {}
values = {}
mem1 = Register(mem1)
def pattern(name, *types):
	def temp(func):
		if func.__name__=="eval":
			evals[name + "".join([str(x) for x in types])] = func
		elif func.__name__=="value":
			values[name + "".join([str(x) for x in types])] = func
	return temp

@pattern("+", Register, int)
def eval(r1, r2):
	return ["add " + str(r1) + " " + str(r2)]

@pattern("+", Register, Register)
def value(r1, r2):
	return mem1

@pattern(":=", Register, Call)
def eval(r1, c2):
	return c2.eval() + ["add " + str(r1) + " " + str(c2.value())]



def eval(name, args, parent):
	temp = name + "".join([str(type(x)) for x in args])
	return evals[temp](*args)
def value(name, args, parent):
	temp = name + "".join([str(type(x)) for x in args])
	if temp in values.keys(): return values[temp](*args)


# print(value("+", [Register("mem2"),Register("asd")]))