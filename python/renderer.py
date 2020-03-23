# Copyright (C) 2019 luna_koly


from moviepy.editor import *

import re
import os

from times import TimeDirective

import logger


def parse_sequences(descriptions, source_file, fontsize=None):
	'''
	Maps marker sequences descriptions
	to clip sequences.
	'''
	source = VideoFileClip(source_file)

	# needed for text-only clips
	resolution = source.size

	# marker -> clip sequence
	sequences = {}

	# proportional font size
	if fontsize == None:
		fontsize = int(resolution[1] / 20)

	for marker in descriptions:
		logger.log(f'Building... [{marker}]')
		sequences[marker] = []

		for it in descriptions[marker]:
			if type(it) is TimeDirective:
				clip = source.subclip(str(it.start), str(it.stop))
				sequences[marker].append(clip)
			else:
				clip = TextClip(it, color='white', method='caption', size=resolution,
								align='center', fontsize=fontsize, font='Arial', bg_color='black')
				clip = clip.set_duration(5)
				sequences[marker].append(clip)

	logger.separate()
	return sequences

def make_pattern(filename):
	'''
	Returns a pattern-filename for
	resulting files.
	'''
	# user provided a pattern
	if re.search(r'\{\}', filename):
		return filename

	# split filename into pieces
	result_file_parts = os.path.splitext(filename)
	extension = os.path.splitext(filename)[1]
	prefix    = os.path.splitext(filename)[0]
	return prefix + '_{}' + extension

def render(descriptions, source_file, result_file, fontsize=None):
	'''
	Saves marker clip sequences to the file.
	'''
	sequences = parse_sequences(descriptions.mapping, source_file, fontsize)
	pattern = make_pattern(result_file)

	for marker in sequences:
		if len(sequences[marker]) == 0:
			continue

		result = concatenate_videoclips(sequences[marker])
		# result = concatenate_videoclips(sequences[marker], method='compose')
		# result = CompositeVideoClip(sequences[marker])
		result.write_videofile(pattern.format(marker))
