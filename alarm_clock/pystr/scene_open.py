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

class SceneOpen(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm open');
			if super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				struct['code'] = 'exit';
				return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				SceneParam._set_msg(struct,self.data['msg']['set_start']);
				#self.send_msg(struct);
				#开始参数设置向导
				self._set_clock_open(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _set_clock_open(self,struct,super_b):
		tnum = 0;
		for ck in super_b.clocks.keys():
			ck = super_b.clocks[ck];
			if ck.has_key('status'):
				status = ck['status'];
				if status['type'] <> 'open':
					tnum = tnum + 1;
					status['type'] == 'open';
		if tnum == 0:
			SceneParam._set_msg(struct,self.data['msg']['no_close_ck']);
		else:
			msg_id = SceneParam._get_random_id(len(self.data['msg']['open_num_ck']));
			struct['result']['msg'] = self.data['msg']['open_num_ck'][msg_id];

