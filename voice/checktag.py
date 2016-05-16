#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
from base import Base
from myexception import MyException
from common import logging

class PM(Base):

	def _check(self,struct):
		try:
			if struct.has_key('Z'): return ;

			inlist = struct['inlist'];
			taglist = struct['taglist'];
			reg = '';
			for _tag in taglist:
				if isinstance(_tag,dict):
					reg = reg + _tag['type'];
				elif _tag in inlist:
					logging.info('unkown the words' + _tag);
			regs = self.data['reg'];
			if reg in regs:
				struct['reg'] = reg;
			else:
				logging.info('can`t find the reg[' + reg + '] from PM file');
		except Exception as e:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			self._check(struct);
		except Exception as e: raise e;

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
