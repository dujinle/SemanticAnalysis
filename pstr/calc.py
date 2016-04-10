#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class Calc(Base):

	def __init__(self):
		self.level = u'低';
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
			flg = False;
			for _str in inlist:
				if struct.has_key(_str):
					strt = struct[_str];
					if strt['type'] == 'C':
						self.level = strt['c'];
						flg = True;
					elif strt['type'] == 'M!':
						if strt['level'] == 'OFF':
							self.level = None;
							continue;
						self.level = strt['level'];
			if not self.level is None:
				struct['value'] = level[self.level];
				if struct.has_key('T'):
					struct['value'] = level[u'中'];
				elif struct.has_key('Z'):
					reg = struct['Z'].get('reg');
					if reg == 'ZX' and flg == False:
						struct['value'] = level[u'中'];
				elif struct.has_key('reg'):
					if struct['reg'] == 'MFX' or struct['reg'] == 'FM':
						struct['value'] = level[u'中'];
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
					elif strt['type'] == 'F':
						if strt['value']['dir'] == 'OFF':
							continue;
						self.dirs = strt['value']['dir'];
					elif strt['type'] == 'M!':
						if strt['dir'] == 'OFF':
							continue;
						self.dirs = strt['dir'];
			struct['dir'] = direct[self.dirs];
			if struct['dir'] == 'NULL':
				self.level = None;
			elif struct['dir'] == 'NEW':
				self.level = u'中';
				struct['dir'] = '+';
			if struct.has_key('T'):
				if struct['dir'] == '+':
					struct['dir'] = '-';
				elif struct['dir'] == '-':
					struct['dir'] = '+';
			if struct.has_key('Z'):
				reg = struct['Z']['reg'];
				if reg == 'ZMFZ':
					self.level = None;
					struct['dir'] = 'NULL';


		except Exception as e:
			raise e;

