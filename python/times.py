# Copyright (C) 2019 luna_koly


import re


SEC_PATTERN = re.compile(r'^(\d+(?:\.\d+)?)$')
MIN_SEC_PATTERN = re.compile(r'^(\d+):(\d+(?:\.\d+)?)$')
H_MIN_SEC_PATTERN = re.compile(r'^(\d+):(\d+):(\d+(?:\.\d+)?)$')

class Time:
	'''
	Represents a time value for h:m:s.
	'''
	def __init__(self, hours=0, minutes=0, seconds=0.0):
		self.seconds = seconds
		self.minutes = minutes
		self.hours = hours

	def __str__(self):
		return str(self.hours) + ':' + str(self.minutes) + ':' + str(self.seconds)

	def total(self):
		'''
		Returns total number of seconds.
		'''
		return self.seconds + self.minutes * 60 + self.hours * 3600

	def increment(self):
		'''
		Increments time value by 1 second.
		'''
		self.seconds += 1

		if self.seconds >= 60:
			difference = self.seconds - 60
			self.seconds = difference
			self.minutes += 1

		if self.minutes >= 60:
			difference = self.minutes - 60
			self.minutes = difference
			self.hours += 1

	@staticmethod
	def parse(string):
		'''
		Builds a new Time instance based on the
		given string representation `h:m:s.f`.
		'''
		match = None
		seconds = 0.0
		minutes = 0
		hours = 0

		def check(pattern):
			nonlocal match
			match = pattern.match(string)
			return match != None

		if check(H_MIN_SEC_PATTERN):
			hours   =   int(match.group(1))
			minutes =   int(match.group(2))
			seconds = float(match.group(3))
		elif check(SEC_PATTERN):
			seconds = float(match.group(1))
		elif check(MIN_SEC_PATTERN):
			minutes =   int(match.group(1))
			seconds = float(match.group(2))
		else:
			return None

		if minutes >= 60:
			raise Exception(f'You can\'t have more than 59 minutes at `{string}`!')

		if seconds >= 60:
			raise Exception(f'You can\'t have >= 60 seconds at `{string}`!')

		return Time(hours, minutes, seconds)


RANGE_PATTERN = re.compile(r'^([\d:.]+)-([\d:.]+)(?:\s+(\w+)\s*|\s*)$')

class TimeDirective:
	'''
	Represents a video range declaration
	'''
	def __init__(self, start, stop, marker):
		self.marker = marker
		self.start = start
		self.stop = stop

	@staticmethod
	def parse(line, increment=False):
		'''
		Returns a TimeDirective if line is
		a valid time directive.
		'''
		match = RANGE_PATTERN.match(line)

		if match == None:
			return None

		marker = match.group(3)

		if marker == None:
			marker = 'main'

		start = Time.parse(match.group(1))
		stop  = Time.parse(match.group(2))

		if increment:
			stop.increment()

		if start.total() >= stop.total():
			duration = stop.total() - start.total()
			raise Exception(f'Are you sure `{duration}` is a good duration?')

		return TimeDirective(start, stop, marker)
