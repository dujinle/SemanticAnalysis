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
import common,alarm_common,pgsql
from common import logging
from myexception import MyException
from base import Base
class SceneSchedule(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene get up');
			if self._if_exist(struct,super_b):
				struct['result']['msg'] = self.data['msg']['ck_exist'][0]
				struct['code'] = 'error';
				logging.info('the alarm clock is exist so add failed!')
				return None;
			if super_b.myclock is None:
				super_b.myclock = dict();
			elif super_b.action is None and super_b.myclock.has_key('time'):
				super_b.myclock = dict();
			self._set_clock(struct,super_b);
		except Exception as e:
			raise MyException(format(e));

	def _set_clock(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			times = struct['ck_time']['time'];
			myclock['type'] = 'getup';
			myclock['time'] = times;
		return 0;

	def _if_exist(self,struct,super_b):
		if struct.has_key('ck_name'):
			ck_name = struct['ck_name'];
			if super_b.clocks.has_key(ck_name): return True;
		if struct.has_key('ck_time'):
			ck_time = struct['ck_time']['time'];
			if super_b.clocks.has_key(ck_time): return True;
		return False;

