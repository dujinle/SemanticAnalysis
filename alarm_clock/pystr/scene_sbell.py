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

#直接设置铃声提示音的场景
class SceneSBell(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm bell');
			if super_b.myclock is None:
				struct['result']['msg'] = self.data['msg']['ck_unknow'][0];
				struct['code'] = 'exit';
				return None;
			if not sturct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				self._encode_bell(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _encode_bell(self,struct,super_b):
		myclock = super_b.myclock;
		for tm in self.data['rings']:
			if tm in struct['inlist']:
				if not myclock.has_key('bell'): myclock['bell'] = dict();
				myclock['bell'].update(self.data['rings'][tm]);
				myclock['bell']['name'] = tm;
				break;
		if myclock.has_key('bell') and myclock['bell'].has_key('name'):
			struct['result']['msg'] = self.data['msg']['set_bell_succ'][0];
		else:
			struct['result']['msg'] = self.data['msg']['bell_unknow'][0];
