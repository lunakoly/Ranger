# Copyright (C) 2019 luna_koly


from descriptions import Descriptions

import os

import renderer
import arrrgh
import logger


if __name__ == '__main__':
	arrrgh.add_flag('help')
	arrrgh.add_alias('h', 'help')

	arrrgh.add_option('input',  'input.mp4')
	arrrgh.add_option('output', 'output.mp4')
	arrrgh.add_option('ranges', 'ranges.rng')

	arrrgh.add_alias('i', 'input')
	arrrgh.add_alias('o', 'output')
	arrrgh.add_alias('r', 'ranges')

	arrrgh.add_integer('fontsize', None)
	arrrgh.add_alias('f', 'fontsize')

	arrrgh.add_option('collect', None)
	arrrgh.add_alias('c', 'collect')

	arrrgh.add_flag('inclusive')
	arrrgh.add_alias('u', 'inclusive')

	arrrgh.parse()

	HELP = arrrgh.options['help']

	INPUT_FILE = arrrgh.options['input']
	OUTPUT_FILE = arrrgh.options['output']
	RANGES_FILE = arrrgh.options['ranges']

	FONTSIZE = arrrgh.options['fontsize']

	COLLECT = arrrgh.options['collect']

	INCLUSIVE = arrrgh.options['inclusive']

	if HELP:
		logger.print_file('help.txt')
		exit(0)

	if not os.path.exists(RANGES_FILE):
		logger.log(f'Error - Ranges file `{RANGES_FILE}` does not exist')
		exit(1)

	if not os.path.exists(INPUT_FILE):
		logger.log(f'Error - Input file `{INPUT_FILE}` does not exist')
		exit(1)

	logger.log('Ranges file - ' + RANGES_FILE)
	logger.log('Input file - ' + INPUT_FILE)
	logger.separate()

	try:
		descriptions = Descriptions.parse(RANGES_FILE, COLLECT, INCLUSIVE)
		renderer.render(descriptions, INPUT_FILE, OUTPUT_FILE, FONTSIZE)
	except Exception as e:
		message, line, line_number, previous_line = e.args
		prefix = f'line {line_number}: '

		logger.separate()
		logger.log(f'Error - {message}')
		logger.separate()

		if previous_line != None:
			previous_number = str(line_number - 1)

			if len(previous_number) < len(str(line_number)):
				previous_number = ' ' + previous_number

			print(f'line {previous_number}: {previous_line}')

		print(prefix + line)
		print(' ' * len(prefix) + '~' * len(line))

		exit(1)
