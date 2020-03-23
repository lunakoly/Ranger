# Copyright (C) 2019 luna_koly


from times import TimeDirective

import logger


class Descriptions:
	'''
	Represents marker sequences descriptions.
	'''
	def __init__(self, collector=None):
		self.mapping = {
			'main': []
		}

		if collector != None and collector != 'main':
			self.mapping[collector] = []

		self.collector = collector

	def ensure_entry(self, marker):
		'''
		Adds an empty list to marker entry if
		there's no any one.
		'''
		if marker not in self.mapping:
			self.mapping[marker] = []

	def add(self, item, marker='main'):
		'''
		Just for making code prettier.
		'''
		self.mapping[marker].append(item)

	def add_title(self, text, marker='main'):
		'''
		Just for making code prettier.
		'''
		logger.log(f'[{marker}] - Title - {text}')
		return self.add(text, marker)

	def add_video(self, tokens, marker='main'):
		'''
		Just for making code prettier.
		'''
		logger.log(f'[{marker}] - Video - {tokens.start}-{tokens.stop}')
		return self.add(tokens, marker)

	def put_title(self, text, marker='main'):
		'''
		Just for making code prettier.
		'''
		self.add_title(text, marker)

		if self.collector != None and self.collector != marker:
			self.add_title(text, self.collector)

	def put_video(self, tokens):
		'''
		Just for making code prettier.
		'''
		self.add_video(tokens, tokens.marker)

		if self.collector != None and self.collector != tokens.marker:
			self.add_video(tokens, self.collector)

	@staticmethod
	def parse(ranges_file, collector=None, inclusive=False):
		'''
		Parses file contents into marker sequences
		descriptions instance.
		'''
		descriptions = Descriptions(collector)

		# remembers text clips and
		# attaches them to the marker of the
		# next video portion
		next_texts = []

		previous_line = None
		line_number = 0

		with open(ranges_file, encoding='utf-8') as ranges:
			for line in ranges:
				line = line.rstrip()

				line_number += 1

				# skip separators
				if len(line) != 0:
					tokens = None

					try:
						tokens = TimeDirective.parse(line, inclusive)
					except Exception as e:
						raise Exception(str(e), line, line_number, previous_line)

					# not a range
					if tokens == None:
						next_texts.append(line)
					else:
						# no marker entry
						descriptions.ensure_entry(tokens.marker)

						# checkout texts
						for it in next_texts:
							descriptions.put_title(it, tokens.marker)

						next_texts.clear()
						descriptions.put_video(tokens)

				previous_line = line

		# checkout last texts to main
		for it in next_texts:
			descriptions.put_title(it, 'main')

		print()
		return descriptions
