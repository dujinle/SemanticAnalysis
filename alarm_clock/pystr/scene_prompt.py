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

from base import Base
#闹铃提示方式设置
class ScenePrompt(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm prompt');
			if super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				struct['code'] = 'exit';
				return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				SceneParam._set_msg(struct,self.data['msg']['set_start']);
				#self.send_msg(struct);
				#开始参数设置向导
				self._set_clock_prompt(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _set_clock_prompt(self,struct,super_b):
		myclock = super_b.myclock;
		if struct['ttag'].find('_only_call_once') <> -1:
			myclock['prompt'] = dict();
			myclock['prompt']['type'] = 'once';
		elif struct['ttag'].find('_call_wake_till') <> -1:
			myclock['prompt'] = dict();
			myclock['prompt']['type'] = 'last';
		SceneParam._set_msg(struct,self.data['msg']['set_prompt_succ']);

