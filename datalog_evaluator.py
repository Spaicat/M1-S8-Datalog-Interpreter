from datalog_data_structure import *
from datalog_parser import *

def is_variable_or_constant(term):
	return isinstance(term, Variable) or isinstance(term, Number) or isinstance(term, Atom)

def unify_variable(var, term, subst):
	"""
	Unify a variable to a term in the subst dictionnary.

	Example:
	>>> subst = {}
	>>> subst = unify_variable(Variable("X"), Number(3), subst)
	>>> subst = unify_variable(Variable("X"), Variable("Y"), subst)
	>>> print(subst)
	{'X': Variable("Y"), 'Y': Number(3)}
	"""

	if (not isinstance(var, Variable)):
		raise Exception("The first parameter should be a variable.")
	elif (var.name == "_"):
		return subst
	elif (var.name in subst):
		return unify(subst[var.name], term, subst)
	elif (isinstance(term, Variable) and term.name in subst):
		return unify(var, subst[term.name], subst)
	else:
		return { **subst, var.name: term }

def unify(t1, t2, subst=None):
	"""
	Unify two terms and return the subst if it's possible.
	
	Returns a set that unify the two terms or False if they can't be unified.
	{} is different from False because {} is a valid unification.

	https://tutorialforbeginner.com/ai-unification-in-first-order-logic

	Example:
	>>> print(unify(Variable("X"), Number(3)))
	{'X': Number(3)}
	>>> print(unify(
	... 	Compound("f", [Variable("X"), Number(3)]),
	... 	Compound("f", [Number(2), Variable("Y")])
	... ))
	{'X': Number(2), 'Y': Number(3)}
	"""
	if (subst is False):
		return False
	elif (subst is None):
		subst = {}

	if (is_variable_or_constant(t1) or is_variable_or_constant(t2)):
		if (t1 == t2):
			return subst
		elif (isinstance(t1, Variable)):
			return unify_variable(t1, t2, subst)
		elif (isinstance(t2, Variable)):
			return unify_variable(t2, t1, subst)
		else:
			return False
	elif (isinstance(t1, Compound) and isinstance(t2, Compound)):
		if (t1.get_functor() != t2.get_functor() or len(t1.arguments) != len(t2.arguments)):
			return False

		for t1_arg, t2_arg in zip(t1.arguments, t2.arguments):
			subst = unify(t1_arg, t2_arg, subst)
		return subst
	else:
		return False

