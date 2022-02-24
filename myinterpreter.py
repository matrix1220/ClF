from myast import *
from lark import Lark, Tree, Token
#print("asd")
def visit(obj, parent=None):
  if type(obj)==Tree:
    if obj.data == "program":
      pass
    elif obj.data == "declassign":
      parent.variables[obj.children[0].value] = visit(obj.children[1])
    elif obj.data == "declfunc":
      p = Function()
      parent.variables[obj.children[1].value] = p
      p.parent = parent
      p.name = obj.children[1].value
      p.content = visit(obj.children[4], p)
    elif obj.data == "declblock":
      generic_visit(obj, parent)
    elif obj.data == "funcparams":
      p = {}
      for k, v in generic_visit(obj, parent):
        p[k] = v
      return p
    elif obj.data == "funcparam":
      return visit(obj.children[0], parent), visit(obj.children[1], parent)
    elif obj.data[0:4] == "stmt":
      tmp = obj.data[4:]
      if tmp == "if":
        p = ifStatement(parent)
      elif tmp == "block":
        p = Block(parent)
      else:
        p = Statement(tmp, parent)
      p.content = generic_visit(obj, p)
      return p
    elif obj.data[0:4] == "cond":
      if len(obj.data)==4:
        p = visit(obj.children[0], parent)
        return p
      else:
        p = Condition(obj.data[4:], parent)
        p.content = generic_visit(obj, p)
        return p
    elif obj.data[0:4] == "expr":
      if len(obj.data)==4:
        p = visit(obj.children[0], parent)
        return p
      else:
        p = Expression(obj.data[4:], parent)
        p.content = generic_visit(obj, p)
        return p
    elif obj.data == "idfind":
      p = find(obj.children[0].value)
      if p is not None: return p
      p = Find(parent, obj.children[0].value)
      return p
    elif obj.data == "idget":
      p = Find(visit(obj.children[0], parent), obj.children[1].value)
      return p
    elif obj.data == "call":
      pass
      #p = Call(parent)
      #p.id = visit(obj.children[0], p)
    elif obj.data == "stmtmove":
      pass
    elif obj.data == "stmtmove":
      pass
  elif type(obj)==Token:
    if obj.type in ["STRING", "NAME", "TYPE", "VAR"]:
      return obj.value
    elif obj.type == "SIGNED_NUMBER":
      return Integer(obj.value)
    # elif obj.type == "VAR":
    #   return parent.getvar(obj.value)

def generic_visit(obj, parent=None):
  return [visit(x, parent) for x in obj.children]

parser = Lark.open("mylang.lark", start='program')
text = open("example.txt", "r").read()
tr = parser.parse(text)
p = Program("example")
generic_visit(tr, p)
print("\n".join(p.eval()+['nop']))