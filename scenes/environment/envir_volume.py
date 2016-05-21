#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from common import logging
from myexception import MyException
import com_funcs as ComFuncs
from scene_base import SceneBase

#处理温度模块
class EnvirVolume(SceneBase):

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('en_scene'): return None;
			if struct['en_scene'] <> 'volume': return None;
			logging.info('go into env volume ......');
			if not struct.has_key('step'): struct['step'] = 'start';
			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'None':
					ComFuncs._set_msg(struct,self.data['msg']['unknow']);
				elif func == '--5':
					self._reduce_volume_value(struct,super_b,'-',0.05);
				elif func == '--10':
					self._reduce_volume_value(struct,super_b,'-',0.10);
				elif func == '++5':
					self._reduce_volume_value(struct,super_b,'+',0.05);
				elif func == '++10':
					self._reduce_volume_value(struct,super_b,'+',0.10);
				elif func == 'max':
					self._reduce_volume_value(struct,super_b,'v',100);
				elif func == 'min':
					self._reduce_volume_value(struct,super_b,'v',0.01);
				else:
					ComFuncs._set_msg(struct,self.data['msg']['unknow']);

			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _reduce_volume_value(self,struct,super_b,tdir,value):
		struct['result']['volume'] = dict();
		struct['result']['volume']['dir'] = tdir;
		struct['result']['volume']['value'] = value;
		ComFuncs._set_msg(struct,self.data['msg']['set_succ']);
