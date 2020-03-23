# Copyright (C) 2019 luna_koly
#
# This scripts simplifies input arguments
# management.


import sys


processors = {
	# option name -> processor function
}

options = {
	# option name -> default value
}

aliases = {
	# alias name -> option name
}

parameters = [
	# `free` arguments passed to the command line
]


# assigns True to an option
def flag_processor(generator, old_value):
	return True

# attempts to assign the next
# argument value to an option
def single_argument_processor(generator, old_value):
	try:
		return next(generator)
	except:
		return old_value

# collects all values of the same option
# that is being called multiple times
# together into a list
def list_processor(generator, old_value):
	try:
		return old_value + [next(generator)]
	except:
		return old_value

# attempts to assign the next
# argument value to an option
# if it's an integer. Otherwise
# leaves the default value as is
def integer_processor(generator, old_value):
	value = None

	try:
		value = next(generator)
	except:
		return old_value

	try:
		return int(value)
	except:
		print("Warning > Ignoring value '" + value + "' because it's not an integer")
		return old_value

# attempts to assign the next
# argument value to an option
# if it's a float. Otherwise
# leaves the default value as is
def float_processor(generator, old_value):
	value = None

	try:
		value = next(generator)
	except:
		return old_value

	try:
		return float(value)
	except:
		print("Warning > Ignoring value '" + value + "' because it's not a float")
		return old_value


# registers a new option
def add_option(name, default_value='', processor=single_argument_processor):
	processors[name] = processor
	options[name] = default_value

# registers a new boolean option
def add_flag(name):
	add_option(name, False, processor=flag_processor)

# registers a new list option
def add_list(name):
	add_option(name, [], processor=list_processor)

# registers a new integer option
def add_integer(name, default_value=0):
	add_option(name, default_value, processor=integer_processor)

# registers a new integer option
def add_float(name, default_value=0):
	add_option(name, default_value, processor=float_processor)

# registers a new alias.
# requires an option to exist
def add_alias(alias_name, option_name):
	if option_name not in options:
		raise Exception('Error > Can\'t create alias for non-existing option > ' + str(option_name))

	aliases[alias_name] = option_name


# returns arguments one by one
def get_next_argument(stream):
	for it in stream:
		yield it

# treates the next generator item as
# an option value and puts it into options
def parse_option(option, generator):
	if option not in options:
		raise Exception('Error > Unspecified option met > ' + str(option))

	options[option] = processors[option](generator, options[option])

# treates the next generator item as
# an alias value and puts it into options
def parse_alias(alias, generator):
	if alias not in aliases:
		raise Exception('Error > Unspecified alias met > ' + str(alias))

	parse_option(aliases[alias], generator)

# fills in the options
def parse(stream=sys.argv):
	generator = get_next_argument(stream)

	for it in generator:
		# option
		if it.startswith('--'):
			parse_option(it[2:], generator)
		# alias
		elif it.startswith('-'):
			for that in it[1:]:
				parse_alias(that, generator)
		# other
		else:
			parameters.append(it)
