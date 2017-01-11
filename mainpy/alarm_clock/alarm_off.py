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

#关闭闹钟
from base import Base
class AlarmOff(Base):

	#---------------------------
	#7点40分的闹钟不要响了
	#7点40分不要叫我了
	#关闭7点40分的闹钟
	#---------------------------
	def encode(self,struct,super_b):
		try:
			if not struct.has_key('clocks'): return None;
			clocktag = 0;
			clocks = struct['clocks'];
			for ck in clocks:
				if ck['type'] == 'all':
					clocktag = clocktag | (1 << 1);
				elif ck['type'] == 'clock':
					clocktag = clocktag | (1);
			if clocktag > 1:
				for ck,cv in super_b.clocks.items():
					cv['status'] = 'off';
			elif clocktag == 1:
				if super_b.myclock is None:
					struct['result']['msg'] = self.data['not_found_ring'];
				else:
					super_b.myclock['status'] = 'off';
					struct['result']['msg'] = self.data['off_ring_succ'];
		except Exception as e:
			raise MyException(format(e));
