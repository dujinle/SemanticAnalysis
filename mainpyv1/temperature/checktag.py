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

class PM(Base):

	def _check(self,struct):
		try:
			self.check_input(struct);
			if struct.has_key('Z'): return ;
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			reg = '';
			for _tag in taglist:
				if type(_tag) == dict:
					reg = reg + _tag['type'];
				elif _tag in inlist:
					raise MyException('the word' + _tag + 'is unknow');
			regs = self.data['reg'];
			if reg in regs:
				struct['reg'] = reg;
			else:
				raise MyException('can`t find the reg[' + reg + '] from PM file');
		except Exception as e:
			raise MyException(format(e));

	def encode(self,struct):
		try:
			self._check(struct);
		except Exception as e:
			raise MyException(format(e));

	def _add(self,data):
		try:
			fdata = self.data;
			regs = fdata.get('reg');
			if data.has_key('value'):
				value = data.get('value');
				if value in regs:
					return;
				regs.append(value);
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			fdata = self.data;
			regs = fdata.get('reg');
			invalue = data.get('value');
			if invalue in regs:
				idx = regs.index(invalue);
				del regs[idx];
		except Exception as e:
			raise MyException(format(e));
