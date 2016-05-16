#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
from base import Base
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
			raise e;

	def calc_level(self,struct):
		try:
			inlist = struct['inlist'];
			level = self.data['value'];
			taglist = struct['taglist'];
			for _tag in taglist:
				if type(_tag) != dict: continue;
				if _tag['type'] == 'C':
					self.level = _tag['level'];
			if not level.has_key(self.level):
				logging.error('Num file has not level key[' + self.level + ']');
				return None;
			struct['value'] = level[self.level];
			if struct.has_key('Nt'):
				struct['value'] = struct['Nt']['value'];
			if struct.has_key('M1') and struct['M1']['reg'].find(u'连') <> -1:
				struct['value'] = '10%';

		except Exception as e:
			raise MyException(sys.exc_info());

	def calc_dir(self,struct):
		try:
			inlist = struct['inlist'];
			direct = self.data['direct'];
			taglist = struct['taglist'];
			mydir = None;
			for _tag in taglist:
				if type(_tag) != dict: continue;
				if _tag.has_key('dir') and _tag['dir'] != 'OFF':
					mydir = _tag['dir'];
					break;

			if struct.has_key('F1'):
				if struct['F1']['dir'] != 'OFF':
					mydir = struct['F1']['dir'];
				#if not mydir is None and struct['F1']['dir'] != u'值':
					#mydir = struct['F1']['dir'];

			if struct.has_key('M1'):
				if mydir is None and struct['M1']['dir'] != 'OFF':
					mydir = struct['M1']['dir'];
			if struct.has_key('Z'):
				if struct['Z']['dir'] != 'OFF':
					mydir = struct['Z']['dir'];

			if not mydir is None: self.dirs = mydir;
			if not direct.has_key(self.dirs):
				logging.error('Num file has not the dir key[' + self.dirs + ']');
				return None;
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
			raise MyException(sys.exc_info());

