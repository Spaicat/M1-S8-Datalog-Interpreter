##########################################
#### Datalog data structure in Python ####
##########################################
"""
Logic terms:
- Atom: Represents a constant atom indentified by a lowercase letter (e.g. tom, john, ...)
- Number: Represents a constant number (e.g. 1, 2, ...)
- Variable: Represents a variable identified by an uppercase letter (e.g. X, Y, ...)
- Compound: Represents a list of terms (e.g. parent(X, Y), father(john, X), ...)

Examples:
>>> x
Atom("x")
>>> 1
Number(1)
>>> X
Variable("X")
>>> parent(X, Y)
Compound("parent", (Variable("X"), Variable("Y")))
>>> father(john, X)
Compound("father", (Atom("john"), Variable("X")))
>>> X is Y + 3
Compound("is", (Variable("X"), Compound("+", (Variable("Y"), Number(3)))))
"""

operators = {
	"=",
	"\\=",
	"==",
	"\\==",
	"<",
	">",
	"=<",
	">=",
	"is",
	"+",
	"-",
	"*",
	"/",
	"//",
}

class Term(object):
	"""
	Interface for a term.
	A term is either a constant (Atom or Number), a variable or a compound term.
	"""
	
	def get_arguments(self):
		"""Return the list of arguments."""
		return []
	
	def get_functor(self):
		"""
		Return the functor which represent the name of the function and the arity.
		Example: parent(X, Y), the functor is parent/2.
		"""
		return None

class Atom(Term):
	def __init__(self, name) -> None:
		if (not name[0].islower()):
			raise Exception("Atom name should start with a lowercase letter, got: '" + name + "'")
		self.name = name
	
	def get_functor(self):
		return self.name, 0
	
	def __repr__(self) -> str:
		return "Atom(\"" + self.name + "\")"

	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, other) -> bool:
		return type(other) == Atom and self.name == other.name

class Number(Term):
	def __init__(self, value) -> None:
		if (not value.isnumeric()):
			raise Exception("Number value should be numeric, got: '" + value + "'")
		self.value = value
	
	def __repr__(self) -> str:
		return "Number(" + str(self.value) + ")"

	def __str__(self) -> str:
		return str(self.value)
	
	def __eq__(self, other) -> bool:
		return type(other) == Number and self.value == other.value

class Variable(Term):
	def __init__(self, name) -> None:
		if (not name[0].isupper()):
			raise Exception("Variable name should start with an uppercase letter, got: '" + name + "'")
		self.name = name
	
	def __repr__(self) -> str:
		return "Variable(\"" + self.name + "\")"

	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, other) -> bool:
		return type(other) == Variable and self.name == other.name

class Compound(Term):
	def __init__(self, name, arguments) -> None:
		self.name = name
		self.arguments = arguments
	
	def get_arguments(self):
		return self.arguments
	
	def get_functor(self):
		return self.name, len(self.arguments)
	
	def __repr__(self) -> str:
		return "Compound(\"" + self.name + "\", " + ", ".join(map(repr, self.arguments)) + ")"

	def __str__(self) -> str:
		if self.name in operators:
			return "(" + str(self.arguments[0]) + " " + self.name + " " + str(self.arguments[1]) + ")"
		return self.name + "(" + ", ".join(map(str, self.arguments)) + ")"
	
	def __eq__(self, other) -> bool:
		return (type(other) == Compound and self.name == other.name
			and all(map(lambda x, y: x == y, self.arguments, other.arguments)))

class Rule(object):
	"""
	A rule is a compound term with a body.
	Example: parent(X, Y) :- father(X, Y).
	"""
	def __init__(self, name, arguments, body) -> None:
		self.name = name
		self.arguments = arguments
		self.body = body
	
	def __repr__(self) -> str:
		return "Rule(\"" + self.name + "\", (" + ", ".join(map(repr, self.arguments)) + "), " + ", ".join(map(repr, self.body)) + ")"
	
	def __str__(self) -> str:
		return self.name + "(" + ", ".join(map(str, self.arguments)) + ") :- " + ", ".join(map(str, self.body)) + "."
	
	def __eq__(self, other) -> bool:
		return type(other) == Rule and self.name == other.name and self.arguments == other.arguments and self.body == other.body

class Fact(object):
	"""
	A fact is a rule without body.
	More precisely it's a fact where the body is always true.
	Example: father(john, tom).
	"""
	def __init__(self, name, arguments) -> None:
		self.name = name
		self.arguments = arguments
	
	def __repr__(self) -> str:
		return "Fact(\"" + self.name + "\", " + ", ".join(map(repr, self.arguments)) + ")"
	
	def __str__(self) -> str:
		return self.name + "(" + ", ".join(map(str, self.arguments)) + ")."
	
	def __eq__(self, other) -> bool:
		return type(other) == Fact and self.name == other.name and self.arguments == other.arguments
