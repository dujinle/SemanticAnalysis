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
from base import Base
class AlarmAdd(Base):

	def encode(self,struct,super_b):
		try:
			print 'go into alarm add action';
			if super_b.myclock is None: super_b.myclock = dict();
			self._set_clock(struct,super_b);
			self._analysis(struct,super_b);
		except Exception as e:
			raise MyException(format(e));

	def _set_clock(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			ctime = struct['ck_time'];
			myclock['time'] = ctime['time'];
			del struct['ck_time'];
		if struct.has_key('ck_name') and struct['ck_name'] <> '':
			if not myclock.has_key('time') or myclock['time'] <> struct['ck_name']:
				myclock['name'] = struct['ck_name'];
		if struct.has_key('ck_delay'):
			myclock['delay'] = struct['ck_delay'];
			del struct['ck_delay'];
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];

	def _analysis(self,struct,super_b):
		ck = super_b.myclock;
		if not ck.has_key('time'):
			struct['result']['msg'] = self.data['time'][0];
			return None;
		elif not ck.has_key('delay'):
			struct['result']['msg'] = self.data['delay'][0];
			return None;
		elif not ck.has_key('able'):
			struct['result']['msg'] = self.data['freq'][0];
			return None;
		ck['status'] = 'on';
		struct['result']['msg'] = self.data['add_suc'][0];
		struct['code'] = 'success';
