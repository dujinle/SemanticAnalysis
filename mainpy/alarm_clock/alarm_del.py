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
class AlarmDel(Base):

	def encode(self,struct,super_b):
		try:
			ept = 0;
			for ck in struct['clocks']:
				if ck['type'] == 'except':
					ept = 1;
				elif ck['type'] == 'all':
					ept = 2;
			if ept == 0:
				if self._del_myclock(super_b) == 0:
					struct['result']['msg'] = self.data['del_ring_suc'];
			elif ept == 1:
				if self._del_othclock(super_b) == 0:
					struct['result']['msg'] = self.data['del_ring_suc'];
			elif ept == 2:
				if self._del_allclock(super_b) == 0:
					struct['result']['msg'] = self.data['del_ring_suc'];
		except Exception as e:
			raise MyException(format(e));

	#del myclock#
	def _del_myclock(self,super_b):
		myclock = super_b.myclock;
		if myclock is None: return -1;
		if not super_b.prev_ck is None and super_b.prev_ck['time'] == myclock['time']:
			super_b.prev_ck = None;
		if myclock.has_key('name'):
			del super_b.clocks[myclock['name']];
			super_b.myclock = None;
			return 0;
		for ck,cv in super_b.clocks.items():
			if cv['time'] == myclock['time']:
				del super_b.clocks[ck];
				super_b.myclock = None;
				return 0;
		return -1;

	#del the other clocks except myclock#
	def _del_othclock(self,super_b):
		myclock = super_b.myclock;
		for ck,cv in super_b.clocks.items():
			if cv['time'] == myclock['time']: continue;
			del super_b.clocks[ck];
			return 0;
		return -1;

	def _del_allclock(self,super_b):
		super_b.clocks.clear();
		return 0;

