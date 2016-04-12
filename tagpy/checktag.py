#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
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
				raise ValueError('can`t find the reg[%s] from PM file' % reg);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			self._check(struct);
		except Exception as e:
			raise e;
