class Type:
	pass

class Value:
	pass

class Evalable:
	pass

class Integer(Value):
	def __init__(self, inp):
		self.inp = inp
	def __str__(self):
		return str(self.inp)
	def eval(self, current=1):
		return []
	def value(self):
		return self

class Register(Value):
	def __init__(self, inp):
		self.inp = inp
	def __str__(self):
		return self.inp
	def __eq__(self, other):
		return self.inp == other.inp
	def eval(self, current=1):
		return []
	def value(self):
		return self

def value(v):
	if  isinstance(v, Value):
		return v
	else:
		return v.value()

mem1 = Register("mem1")

class Instruction:
	def __init__(self):
		self.used = []
	def getvar(self, name):
		return self.parent.getvar(name)

class Program:
	def __init__(self, name):
		self.name = name
		self.variables = {}
		self.temps = [mem1, Register("mem2"), Register("mem3")]

	def getvar(self, name):
		return self.variables[name]

	def eval(self, current=1):
		return self.variables["__main__"].eval(current)

class Function:
	def __init__(self):
		self.variables = {}

	def getvar(self, name):
		if name in self.variables.keys(): return self.variables[name]
		else: return self.parent.getvar(name)

	def eval(self, current=1):
		return self.content.eval(current)


class Statement(Instruction):
	class Methods:
		def mov(self, current=1):
			tmp = Evaluator(current, self)
			return tmp.eval() + ["mov " + str(tmp.value()[1]) + " " + str(tmp.value()[0])]
			
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent

	def eval(self, current=1):
		return getattr(self.Methods, self.name)(self, current)

class ifStatement(Statement):
	def __init__(self, parent):
		self.parent = parent

	def eval(self, current=1):
		condition = self.content[0].eval(current)
		current = current + len(condition)
		positive = self.content[1].eval(current+1)
		if len(self.content)==2:
			return condition + ["jmp " + str(current+len(positive)+1)] + positive
		else:
			negative = self.content[2].eval(current + len(positive) + 2)
			return condition + ["jmp " + str(current+len(positive)+2)] + positive + ["jmp " + str(current)] + negative

class Block(Statement):
	def __init__(self, parent):
		self.parent = parent

	def eval(self, current=1):
		result = []
		for temp in self.content:
			temp = temp.eval(current)
			current = current + len(temp)
			result = result + temp
		return result

class Condition(Instruction):
	class Methods:
		def eq(self, current=1):
			tmp = Evaluator(current, self)
			return tmp.eval() + ["teq " + str(tmp.value()[0]) + " " + str(tmp.value()[1])]
			
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent

	def eval(self, current=1):
		return getattr(self.Methods, self.name)(self, current)

class void: pass

import re
def find(inp):
	if re.match(r"mem[1-4][1-4]?", inp):
		return Register(inp)
	elif inp.upper() in ["CLK", "IPT", "CNR", "CNG"]:
		return Register(inp)
	elif inp=="void":
		return void

class Expression(Instruction):
	class Methods:
		def add(self, current=1):
			tmp = Evaluator(current, self)
			return tmp.eval() + ["add " + str(tmp.value()[0]) + " " + str(tmp.value()[1])]
		def mul(self, current=1):
			tmp = Evaluator(current, self)
			return tmp.eval() + ["mul " + str(tmp.value()[0]) + " " + str(tmp.value()[1])]
			
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent

	def value(self):
		return mem1

	def eval(self, current=1):
		return getattr(self.Methods, self.name)(self, current)

class Call(Instruction):
	def __init__(self, content, parent):
		self.content = content
		self.parent = parent

	def value(self):
		return mem1

	def eval(self, current=1):
		return getattr(self.Methods, self.name)(self, current)

class Reference:
	def __init__(self, content, parent):
		self.content = content
		self.parent = parent

	def value(self):
		return self.parent.getvar(self.content)


class Evaluator:
	temps = [mem1, Register("mem2"), Register("mem3")]
	def __init__(self, current, content):
		self.code = []
		self.val = []
		for v in content.content:
			vv = v.value()
			if type(vv)==Register and vv in self.val:
				ff = self.unused()
				self.code += ['mov ' + str(vv) + ' ' + str(ff)]
				self.val[self.val.index(vv)] = ff
				current+=1
			cc = v.eval(current)
			self.code += cc
			current += len(cc)
			self.val += [vv]
	def unused(self):
		newtemp = None
		for temp in Evaluator.temps:
			if temp not in self.val:
				newtemp = temp
				break
		if newtemp is None:
			raise Exception("No enough temporary registers")
		else:
			return newtemp
	def eval(self):
		return self.code
	def value(self):
		return self.val
# print(
#print({"sas":"asd",2:"asd"})