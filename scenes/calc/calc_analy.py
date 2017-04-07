#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

class CalcAnaly(SceneBase):

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

	def _cal_mult(self,struct,super_b):
		nums = list();
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('type') and item['type'] == 'NUM':
				nums.append(item);
		if nums is None or len(nums) <> 2:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			s = int(nums[0]['stype']);
			e = int(nums[1]['stype']);
			re = s * e;
			struct['result']['Math'] = re;
			ComFuncs._set_msg(struct,self.data['msg']['cal_succ'],re);

