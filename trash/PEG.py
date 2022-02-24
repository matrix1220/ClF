from pypeg2 import *

class Key(str):
	grammar = "#", restline, endl

k = parse("#asdasdasd\n#asdasd", (Key, Key))
print(k)