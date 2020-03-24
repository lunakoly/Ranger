# Copyright (C) 2019 luna_koly


import os


# True means that the last
# printed line is an empty one
already_separated = False

def log(pattern, *args):
	'''
	Prints a message to the screen based on the
	given pattern and arguments.
	'''
	global already_separated

	print('Cut - ' + str(pattern).format(*args))
	already_separated = False

def separate():
	'''
	Prints an empty line if the previous
	printed line wasn't empty.
	'''
	global already_separated

	if not already_separated:
		already_separated = True
		print()

def print_file(filename):
	'''
	Writes contents of 'filename' into stdout.
	'''
	directory = os.path.dirname(os.path.realpath(__file__))
	filepath = os.path.join(directory, filename)

	with open(filepath, 'r') as file:
		print(file.read())
