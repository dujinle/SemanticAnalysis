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

class Check(Base):

	def _check(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			reg = '';
			for _tag in taglist:
				if type(_tag) == dict:
					reg = reg + _tag['type'];
				elif _tag in inlist:
					raise ValueError('the word %s is unknow' % _tag);
			regs = self.data['reg'];
			if reg in regs:
				struct['reg'] = reg;
			else:
				raise MyException('can`t find the reg[%s] from PM file' % reg);
		except Exception as e:
			raise MyException(format(e));

	def encode(self,struct):
		try:
			self._check(struct);
		except Exception as e:
			raise MyException(format(e));
