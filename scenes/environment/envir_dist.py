#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from common import logging
from myexception import MyException
import com_funcs as ComFuncs
from scene_base import SceneBase

#区分所属模块
class EnvirDist(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into env dist ......');
			if not struct.has_key('en_scene'):
				func = self._fetch_func(struct);
				if func <> 'None':
					struct['en_scene'] = func;
		except Exception as e:
			raise MyException(sys.exc_info());
