#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from com_base import ComBase as FoodBase
import com_funcs as ComFuncs

#处理 电话短信  场景
class FoodAnalysis(FoodBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into Food analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'food_spot':
					self._get_near_food_info(struct,super_b);
					struct['step'] = 'select';
					return None;
			elif struct['step'] == 'select':
				if func == 'get_more':
					self._get_near_more_info(struct,super_b);
					return None;
				elif func == 'sure':
					ComFuncs._set_msg(struct,self.data['msg']['sure_succ']);
			elif struct['step'] == 'selected':
				ComFuncs._set_msg(struct,self.data['msg']['require']);
				struct['step'] = 'require';
				return None;
			elif struct['step'] == 'require':
				self._get_require_info(struct,super_b);
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

		print reg
		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

	def _get_near_food_info(self,struct,super_b):
		near = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item.has_key('type') and item['type'] == 'SP':
				near = item['str'];
				break;
		if near is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			food = super_b.get_food_by_sp(near);
			if food is None:
				ComFuncs._set_msg(struct,self.data['msg']['unknow']);
				return None;
			struct['result']['Food'] = food;
			ComFuncs._set_msg(struct,self.data['msg']['near_succ'],len(food)," ".join(food));

	def _get_near_more_info(self,struct,super_b):
		food = super_b.get_more_info(self.data['local']);
		if food is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['Food'] = food;
			ComFuncs._set_msg(struct,self.data['msg']['more_succ']);

	def _get_require_info(self,struct,super_b):
		tdic = dict();
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item.has_key('type') and item['type'] == 'TIME':
				tdic['time'] = item['start'];
			elif item.has_key('type') and item['type'] == 'Nunit':
				tdic['rnum'] = item['str'];
			elif item.has_key('type') and item['type'] == 'Nunit':
				pass;
		if not tdic.has_key('time'):
			ComFuncs._set_msg(struct,self.data['msg']['no_time']);
		else:
			struct['result']['Food'] = tdic;
			ComFuncs._set_msg(struct,self.data['msg']['sure_succ']);
		pass;

