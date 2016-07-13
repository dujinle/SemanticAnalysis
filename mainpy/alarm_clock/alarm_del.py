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

class AlarmDel():

	def __init__(self): pass;

	def encode(self,struct,super_b):
		try:
			ept = 0;
			for ck in struct['clocks']:
				if ck['type'] == 'except':
					ept = 1;
				elif ck['type'] == 'all':
					ept = 2;
			if   ept == 0: self._del_myclock(super_b);
			elif ept == 1: self._del_othclock(super_b);
			elif ept == 2: self._del_allclock(super_b);
		except Exception as e:
			raise MyException(format(e));

	#del myclock#
	def _del_myclock(self,super_b):
		myclock = super_b.myclock;
		if myclock is None: return None;
		if myclock.has_key('name'):
			del super_b.clocks[myclock['name']];
			super_b.myclock = None;
			return None;
		for ck,cv in super_b.myclock.items():
			if cv == myclock:
				del super_b.clocks[ck];
				super_b.myclock = None;
				break;

	#del the other clocks except myclock#
	def _del_othclock(self,super_b):
		myclock = super_b.myclock;
		for ck,cv in super_b.myclock.items():
			if cv == myclock: continue;
			del super_b.clocks[ck];

	def _del_allclock(self,super_b):
		super_b.clocks.clear();

