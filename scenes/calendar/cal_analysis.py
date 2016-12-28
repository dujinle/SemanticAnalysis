#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from com_base import ComBase as CalBase
import com_funcs as ComFuncs

#处理 日历详细信息
class CalAnalysis(CalBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into calendar analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';
			if struct['step'] == 'start':
				func = self._fetch_func(struct);
				if func == 'get':
					self._get_time_info(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_func(self,struct):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			reg = reg + item['stype'];
			if item.has_key('child'):
				reg = reg + item['child']['stype'];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

	def _get_time_info(self,struct,super_b):
		time = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item.has_key('type') and item['type'] == 'TIME':
				time = item;
				break;
		if time is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			time_t = super_b.get_time_info(time);
			if time_t is None:
				ComFuncs._set_msg(struct,self.data['msg']['unknow']);
				return None;
			struct['result']['time'] = time_t;
			struct['result']['msg'] = time_t['lunar'];

