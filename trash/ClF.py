class Statement:
	def __init__(self):
		pass
	def getCode(self, current=1):
		pass

class Block(Statement):
	def __init__(self, *args):
		self.contents = args;
	def getCode(self, current = 1):
		result = []
		for temp in self.args:
			temp = temp.getCode(current)
			current = current + len(temp)
			result = result + temp
		return result

class Robject: # runtime
	pass

class Cobject: # compile-time
	pass

class Rinteger:
	pass

class Cinteger:
	pass


class Integer:
	def __init__(self, value):
		self.value = value

	def getValue(self):
		return str(self.value)

class Register:
	def __init__(self, value):
		self.value = value

	def getValue(self):
		return self.value


class Expression:
	def getValue(self):
		pass
	def getCode(self, current=1):
		pass

class Addition(Expression):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def getValue(self):
		return "mem1"

	def getCode(self, current=1):
		return ["add " + self.left.getValue() + " " + self.right.getValue()]

class Assignment(Statement):
	def __init__(self, source, destination):
		self.source = source
		self.destination = destination

	def getCode(self, current=1):
		return self.source.getCode() + ["mov " + self.source.getValue() + " " + self.destination.getValue()]

class Condition:
	pass

class EqualTo(Condition):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def getCode(self, current=1):
		return ["teq " + self.left.getValue() + " " + self.right.getValue()]

class ifStatement(Statement):
	def __init__(self, condition, positive, negative):
		self.condition = condition
		self.positive = positive
		self.negative = negative
	def __init__(self, condition, positive):
		self.condition = condition
		self.positive = positive

	def getCode(self, current=1):
		condition = self.condition.getCode(current)
		current = current + len(condition)
		positive = self.positive.getCode(current+1)
		if not hasattr(self, "negative"):
			return condition + ["jmp " + str(current+len(positive)+1)] + positive
		else:
			negative = self.negative.getCode(current + len(positive) + 2)
			return condition + ["jmp " + str(current+len(positive)+2)] + positive + ["jmp " + str(current)] + negative

print(
	ifStatement(
		EqualTo(Register("mem11"), Integer(6)),
		Assignment(Addition(Integer(4), Register("mem11")), Register("mem22"))
		).getCode()
	)
