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
import common,alarm_common
from myexception import MyException
from common import logging

from base import Base
class SceneStop(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm delay');
			if super_b.myclock is None:
				struct['result']['msg'] = self.data['msg']['ck_unknow'][0];
				struct['code'] = 'exit';
				return None;
			if not sturct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				struct['result']['msg'] = self.data['msg']['set_start'];
				#self.send_msg(struct);
				#开始参数设置向导
				self._set_clock_delay(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _set_clock_delay(self,struct,super_b):
		myclock = super_b.myclock;
		dtag = self.data['deal_tag'];
		for key in dtag:
			if struct['ttag'].find(key) <> -1:
				tag = dtag[key];
				myclock['status'] = dict(tag);
				myclock['status']['type'] = 'delay';
				break;
		if struct['ttag'].find('_time') <> -1:
			inter = struct['intervals'][0];
			if inter['scope'] == 'min' and inter.has_key('value'):
				myclock['status'] = dict();
				myclock['status']['scope'] = 'min';
				myclock['status']['type'] = 'delay';
				myclock['status']['value'] = inter['value'];
		struct['result']['msg'] = self.data['msg']['set_delay_succ'][0];

