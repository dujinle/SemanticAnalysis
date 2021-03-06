#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class Calc(Base):

	def init(self):
		self.level = u'中';
		self.dirs = u'正';

	def encode(self,struct):
		try:
			self.calc_dir(struct);
			self.calc_level(struct);
		except Exception as e:
			raise e;

	def calc_level(self,struct):
		try:
			inlist = struct['inlist'];
			level = self.data['value'];
			taglist = struct['taglist'];
			for _tag in taglist:
				if _tag['type'] == 'C':
					self.level = _tag['level'];
			if struct.has_key('M1'):
				m1 = struct['M1'];
				if m1['reg'].find('C') != -1:
					self.level = u'中';
			struct['value'] = level[self.level];
		except Exception as e:
			raise e;

	def calc_dir(self,struct):
		try:
			inlist = struct['inlist'];
			direct = self.data['direct'];
			taglist = struct['taglist'];
			for _tag in taglist:
				if _tag['type'] == 'F':
					if _tag['dir'] == 'OFF':
						continue;
					self.dirs = _tag['dir'];
				if _tag['type'] == 'X':
					self.dirs = _tag['dir'];
			if struct.has_key('F1'):
				if struct['F1']['dir'] != 'OFF':
					self.dirs = struct['F1']['dir'];
			if struct.has_key('M1'):
				if struct['M1']['dir'] != 'OFF':
					self.dirs = struct['M1']['dir'];
			struct['dir'] = direct[self.dirs];

			if struct['dir'] == 'NEW':
				struct['dir'] = '+';

			if struct.has_key('X1'):
				if struct['X1']['dir'] != 'OFF' and struct['X1']['dir'] == '!':
					if struct['dir'] == '+':
						struct['dir'] = '-';
					elif struct['dir'] == '-':
						struct['dir'] = '+';
		except Exception as e:
			raise e;

