#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
from base import Base
#============================================
''' import MyException module '''

base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
from myexception import MyException

class Calc(Base):

	def init(self):
		self.level = u'中';
		self.dirs = u'正';

	def encode(self,struct):
		try:
			self.calc_dir(struct);
			self.calc_level(struct);
		except Exception as e:
			raise MyException(format(e));

	def calc_level(self,struct):
		try:
			inlist = struct['inlist'];
			level = self.data['value'];
			taglist = struct['taglist'];
			for _tag in taglist:
				if _tag['type'] == 'C':
					self.level = _tag['level'];
			if not level.has_key(self.level):
				raise MyException('Num file has not level key[' + self.level + ']');
			struct['value'] = level[self.level];
			if struct.has_key('Nt'):
				struct['value'] = struct['Nt']['value'];
		except Exception as e:
			raise MyException(format(e));

	def calc_dir(self,struct):
		try:
			inlist = struct['inlist'];
			direct = self.data['direct'];
			taglist = struct['taglist'];
			for _tag in taglist:
				if _tag.has_key('dir') and _tag['dir'] != 'OFF':
					self.dirs = _tag['dir'];
					break;
			if struct.has_key('F1'):
				if struct['F1']['dir'] != 'OFF':
					self.dirs = struct['F1']['dir'];

			if struct.has_key('M1'):
				if self.dirs is None and struct['M1']['dir'] != 'OFF':
					self.dirs = struct['M1']['dir'];

			if not direct.has_key(self.dirs):
				raise MyException('Num file has not the dir key[' + self.dirs + ']');
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
			raise MyException(format(e));

