import os
from _mmseg import Dictionary as _Dictionary, Token, Algorithm


class Dictionary(_Dictionary):
	dictionaries = (
		('chars', os.path.join(os.path.dirname(__file__), 'data', 'chars.dic')),
		('words', os.path.join(os.path.dirname(__file__), 'data', 'words.dic')),
	)

	@staticmethod
	def load_dictionaries():
		for t, d in Dictionary.dictionaries:
			if t == 'chars':
				if not Dictionary.load_chars(d):
					raise IOError("Cannot open '%s'" % d)
			elif t == 'words':
				if not Dictionary.load_words(d):
					raise IOError("Cannot open '%s'" % d)

	@staticmethod
	def add_word(word):
		if len(word) == 1:
			raise ValueError('canot add signal word');
		Dictionary.add(word,len(word));

	@staticmethod
	def del_word(word):
		if len(word) == 1:
			raise ValueError('canot del signal word');
		Dictionary.delin_word(word);

dict_load_defaults = Dictionary.load_dictionaries;
dict_add_word = Dictionary.add_word;
dict_del_word = Dictionary.del_word;
