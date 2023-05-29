#######################################
#### Datalog Interpreter in Python ####
#######################################

import sys
from datalog_parser import parse

def read_file(filename):
	"""Opens the file, removes the new line character and return the content list."""
	try:
		with open(filename, "r") as file:
			return file.read()
	except FileNotFoundError:
		raise Exception("The specified file was not found.")
	except IOError:
		raise Exception("An error occurred while reading the file.")

def main(argv):
	print("Executing Datalog Interpreter...")

	if len(argv) == 0 or len(argv) > 1:
		print("Incorrect number of arguments.")
		print("Usage: py interpret.py <filename>")
		return
	
	try:
		content = read_file(argv[0])
		rules = parse(content)
		
		for rule in rules:
			print(repr(rule))
		
	except Exception as e:
		raise e
	except:
		print("An unexpected error has occurred.")

if __name__ == "__main__":
	main(sys.argv[1:])
