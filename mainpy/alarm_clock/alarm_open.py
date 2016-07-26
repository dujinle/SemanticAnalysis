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

class AlarmOpen():

	def __init__(self): pass;

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('clocks'):
				struct['code'] = 'error';
				return None;
			clocktag = 0;
			clocks = struct['clocks'];
			for ck in clocks:
				if ck['type'] == 'all':
					clocktag = clocktag | (1 << 1);
				elif ck['type'] == 'clock':
					clocktag = clocktag | (1);
			if clocktag > 1:
				for ck,cv in super_b.clocks.items():
					cv['status'] = 'open';
			elif clocktag == 1:
				if super_b.myclock is None:
					struct['code'] = 'error';
				else:
					super_b.myclock['status'] = 'open';
					self._modify_clock(struct,super_b);
		except Exception as e:
			raise MyException(format(e));

	#modify clock attribute#
	def _modify_clock(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('adjust_date'):
			atime = struct['adjust_date'];
			[hour,min] = myclock['time'].split(':');
			ihour = int(hour);
			imin = int(min);
			if atime['dir'] == '-':
				if imin < int(atime['level']):
					ihour = ihour - 1;
					imin = imin - int(atime['level']) + 60;
				else:
					imin = imin - int(atime['level'])
			elif atime['dir'] == '+':
				if imin + int(atime['level']) >= 60:
					ihour = ihour + 1;
					imin = imin + int(atime['level']) - 60;
				else:
					imin = imin + int(atime['level']);
			myclock['time'] = str(ihour) + ':' + str(imin);
			del struct['adjust_date'];
		elif struct.has_key('ck_delay'):
			myclock['delay'] = struct['ck_delay'];
			del struct['ck_delay'];
		elif struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
		elif struct.has_key('ck_time'):
			myclock['time'] = struct['ck_time']['time'];
			del struct['ck_time'];
		elif struct.has_key('ck_bell'):
			myclock['bell'] = struct['ck_bell'];
			del struct['ck_bell'];

