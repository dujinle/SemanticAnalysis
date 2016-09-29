#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
from myexception import MyException
from common import logging
import scene_param as SceneParam

from scene_base import SceneBase

class SceneStop(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm stop');
			if super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				struct['code'] = 'exit';
				return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				SceneParam._set_msg(struct,self.data['msg']['set_start']);
				#self.send_msg(struct);
				#开始参数设置向导
				self._set_clock_stop(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _set_clock_stop(self,struct,super_b):
		myclock = super_b.myclock;
		myclock['status'] = dict();
		myclock['status']['type'] = 'stop';
		SceneParam._set_msg(struct,self.data['msg']['set_stop_succ']);

