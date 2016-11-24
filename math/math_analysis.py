#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from math_base import MathBase
import com_funcs as ComFuncs

#处理 电话短信  场景
class MathAnalysis(MathBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into Math analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				func = self._fetch_func(struct);
				if func == 'multiply':
					self._cal_mult(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_func(self,struct):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			reg = reg + struct[istr]['stype'];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

	def _cal_mult(self,struct,super_b):
		nums = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item.has_key('type') and item['stype'] == 'MULTIPLY':
				if item.has_key('nums'):
					nums = item['nums'];
					break;
		if nums is None or len(nums) <> 2:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			s = int(nums[0]['stype']);
			e = int(nums[1]['stype']);
			re = s * e;
			struct['result']['Math'] = re;
			ComFuncs._set_msg(struct,self.data['msg']['cal_succ'],re);

