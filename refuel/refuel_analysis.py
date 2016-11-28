#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from refuel_base import RefuelBase
import com_funcs as ComFuncs

#处理 电话短信  场景
class RefuelAnalysis(RefuelBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into Refuel analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'refuel':
					self._get_refuel_info(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_func(self,struct):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			reg = reg + item['stype'];
			if item.has_key('child'): reg = reg + item['child']['stype'];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

	def _get_refuel_info(self,struct,super_b):
		ComFuncs._set_msg(struct,self.data['msg']['refuel_info']);
		return None;

