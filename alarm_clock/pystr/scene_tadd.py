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
import common,pgsql
from common import logging
from myexception import MyException
from base import Base
class SceneTadd(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene time add action......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				struct['result']['msg'] = self.data['msg']['start_msg'];
				super_b.myclock = dict();
				#todo send msg......
			self._find_time(struct);
			self._calc_able(struct);
			self._set_time(struct,super_b);
			struct['step'] = 'trans';
		except Exception as e:
			raise MyException(format(e));

	def _set_time(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			times = struct['ck_time']['time'];
			hour = int(times.split(':')[0]);
			if hour >= self.data['common']['getup_time'][0] \
				and hour <= self.data['common']['getup_time'][1]:
				struct['ck_scene'] = 'ck_getup_add';
				myclock['type'] = 'getup';
				#时间设置完成回应信息
				struct['result']['msg'] = self.data['msg']['add_getup_ck'];
				#todo send msg......
			else:
				struct['ck_scene'] = 'ck_schedule_add';
				myclock['type'] = 'schedule';
				#时间设置完成回应信息
				struct['result']['msg'] = self.data['msg']['add_schedule_ck'];
				#todo send msg......
			myclock['time'] = struct['ck_time']['time'];
			del struct['ck_time'];
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
		return 0;

