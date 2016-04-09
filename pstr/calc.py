#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class Calc(Base):

	def __init__(self):
		self.level = u'低';
		self.dirs = u'正';

	def encode(self,struct):
		try:
			self.calc_level(struct);
			self.calc_dir(struct);
		except Exception as e:
			raise e;

	def calc_level(self,struct):
		try:
			inlist = struct['inlist'];
			level = self.data['value'];
			for _str in inlist:
				if struct.has_key(_str):
					strt = struct[_str];
					if strt['type'] == 'C':
						self.level = strt['c'];
						break;
			struct['value'] = level[self.level];
		except Exception as e:
			raise e;

	def calc_dir(self,struct):
		try:
			inlist = struct['inlist'];
			direct = self.data['direct'];
			for _str in inlist:
				if struct.has_key(_str):
					strt = struct[_str];
					if strt['type'] == 'X':
						self.dirs = strt['dir'];
						break;
			struct['dir'] = direct[self.dirs];
			if struct.has_key('T'):
				if struct['dir'] == '+':
					struct['dir'] = '-';
				elif struct['dir'] == '-':
					struct['dir'] = '+';

		except Exception as e:
			raise e;

