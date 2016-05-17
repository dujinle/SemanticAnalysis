#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
from base import Base
from common import logging
from myexception import MyException

class PM(Base):

	def _check(self,struct):
		try:
			if struct.has_key('Z'): return ;
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			reg = '';
			for _tag in taglist:
				if type(_tag) == dict:
					reg = reg + _tag['type'];
				elif _tag in inlist:
					logging.error('the word' + _tag + 'is unknow');
			regs = self.data['reg'];
			if reg in regs:
				struct['reg'] = reg;
			else:
				logging.error('can`t find the reg[' + reg + '] from PM file');
				return None;
		except Exception as e:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			self._check(struct);
		except Exception as e:
			raise e;

	def _add(self,data):
		try:
			fdata = self.data;
			regs = fdata.get('reg');
			if data.has_key('value'):
				value = data.get('value');
				if value in regs: return None;
				regs.append(value);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _del(self,data):
		try:
			fdata = self.data;
			regs = fdata.get('reg');
			invalue = data.get('value');
			if invalue in regs:
				idx = regs.index(invalue);
				del regs[idx];
		except Exception as e:
			raise MyException(sys.exc_info());
