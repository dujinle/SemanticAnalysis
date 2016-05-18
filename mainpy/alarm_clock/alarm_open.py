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
class AlarmOpen(Base):

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
					cv['status'] = 'open';
			elif clocktag == 1:
				if super_b.myclock is None:
					struct['result']['msg'] = self.data['not_found_ring'];
				else:
					super_b.myclock['status'] = 'on';
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
			struct['result']['msg'] = self.data['mo_time_suc'][0];
		if struct.has_key('ck_delay'):
			myclock['delay'] = struct['ck_delay'];
			struct['result']['msg'] = self.data['mo_ring_type'][0];
			del struct['ck_delay'];
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			struct['result']['msg'] = self.data['mo_ring_able'][0];
			del struct['ck_able'];
		if struct.has_key('ck_time'):
			myclock['time'] = struct['ck_time']['time'];
			struct['result']['msg'] = self.data['mo_time_suc'][0];
			del struct['ck_time'];
		if struct.has_key('ck_bell'):
			myclock['bell'] = struct['ck_bell'];
			struct['result']['msg'] = self.data['mo_ring_bell'][0];
			del struct['ck_bell'];

