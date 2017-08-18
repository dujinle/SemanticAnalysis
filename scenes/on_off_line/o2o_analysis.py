#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from com_base import ComBase as O2oBase
import com_funcs as ComFuncs

#处理 O2O信息
class O2oAnalysis(O2oBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into O2o analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'home_keep':
					self._get_home_keep(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _get_home_keep(self,struct,super_b):
		homek = super_b.get_home_keep();
		struct['result']['hk'] = homek;
		ComFuncs._set_msg(struct,self.data['msg']['homek_succ']);
		return None;
