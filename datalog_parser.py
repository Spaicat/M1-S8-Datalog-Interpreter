import re
from datalog_data_structure import *

# Match words (group of letters/numbers) or symbols
# Each match will be a token
TOKENIZER_REGEX = r"[a-zA-Z0-9_]+|[.,()]|:-|<=|>=|==|\\=|\\==|\+|\-|\*|\\|[=><]"

# (?<!\\) : check if there is no backslash before the %
# (?![^"]*"[^"]*(?:"[^"]*"[^"]*)*$) : check if the % is not in a string (between quotes)
# (.*) : match the rest of the line
COMMENT_REGEX = r"(?<!\\)%(?![^\"]*\"[^\"]*(?:\"[^\"]*\"[^\"]*)*$)(.*)"

OPERATOR_REGEX = r"^is|<=|>=|==|\\=|\\==|\+|\-|\*|\\|[=><]$"
VARIABLE_REGEX = r"^[A-Z_][a-zA-Z0-9_]*$"
ATOM_REGEX = r"^[a-z][a-zA-Z0-9_]*$"
NUMBER_REGEX = r"^[0-9]+$"
TERM_REGEX = r"^[a-zA-Z0-9_]+$"

def remove_comment(text):
	"""Removes the comments `% ... \n` from the datalog content list."""
	return re.sub(COMMENT_REGEX, "", text, 0, re.MULTILINE)

def tokenize(text):
	"""Split the text into a list of tokens that we can iterate after."""
	text = text.replace("\n", "")
	ite = re.finditer(TOKENIZER_REGEX, text)
	return [token.group() for token in ite]

def parse_args(tokens):
	"""Return a list of arguments."""
	args = []
	
	while (tokens[0] != ")"):
		args.append(parse_term(tokens))

		if (tokens[0] not in (",", ")")):
			raise Exception("Should be a ',' or a ')' after an argument but got: '" + tokens[0] + "'")
		if (tokens[0] == ","): tokens.pop(0) # skip ","
	tokens.pop(0) # skip ")"

	return args

def parse_head(tokens):
	"""
	Return a temporary object that will be used to create a rule or a fact
	"""
	name = tokens.pop(0)
	args = []

	tokens.pop(0) # skip "("
	args = parse_args(tokens)

	return (name, args)

def parse_term(tokens):
	"""
	Parse a term which can be a variable, a number, an atom or a compound
	"""
	name = tokens[0]
	if (len(tokens) > 1):
		name = tokens.pop(0)
	
	# Check if the term is an operator and make it a compound if it is
	# TODO: Check precedence of operators
	if (re.match(OPERATOR_REGEX, tokens[0]) is not None):
		op = tokens.pop(0) # skip the operator
		return Compound(op, [parse_term(name), parse_term(tokens)])
			
	if (re.match(VARIABLE_REGEX, name) is not None):
		if (name == "_"):
			return Variable("_")

		return Variable(name)

	if (re.match(NUMBER_REGEX, name) is not None):
		return Number(name)
	
	if (re.match(ATOM_REGEX, name) is not None and tokens[0] != "("):
		return Atom(name)

	tokens.pop(0) # skip "("
	args = parse_args(tokens)
	return Compound(name, args)

def parse_rule(tokens):
	"""Return a rule or a fact."""
	head = parse_head(tokens)

	if (tokens[0] == "."):
		tokens.pop(0) # skip "."
		return Fact(head[0], head[1])
	elif (tokens[0] != ":-"):
		raise Exception("Should be a '.' or a ':-' after a head but got: '" + tokens[0] + "'")
	tokens.pop(0) # skip ":-"

	tail = []
	while (tokens[0] != "."):
		tail.append(parse_term(tokens))
		if (tokens[0] not in (",", ".")):
			raise Exception("Should be a ',' or a '.' after a term but got: '" + tokens[0] + "'")
		if (tokens[0] == ","): tokens.pop(0) # skip ","
	
	tokens.pop(0) # skip "."
	return Rule(head[0], head[1], tail)

def parse(text):
	# Object that will let us iterate over the tokens
	tokens = tokenize(remove_comment(text))
	print(tokens)

	rules = []
	
	while (len(tokens) > 0):
		rules.append(parse_rule(tokens))
	
	return rules
