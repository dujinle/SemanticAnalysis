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
class AlarmModify(Base):

	def encode(self,struct,super_b):
		try:
			print 'go into action modify';
			if super_b.myclock is None:
				struct['result']['msg'] = self.data['not_found_ring'][0];
				struct['result']['extra'] = self.data['not_found_ringe'][0];
				struct['code'] = 'exit';
				return None;
			for ck in struct['clocks']:
				if ck['type'] == 'qdelay':
					struct['question'] = 'delay';
				elif ck['type'] == 'bell':
					struct['question'] = 'bell';
				elif ck['type'] == 'qable':
					struct['question'] = 'able';
				elif ck['type'] == 'time':
					struct['question'] = 'time';
			self._modify_clock(struct,super_b);
			self._analysis_clock(struct,super_b);
		except Exception as e:
			raise MyException(format(e));

	#modify clock attribute#
	def _modify_clock(self,struct,super_b):
		myclock = super_b.myclock;
		set_suc = False;
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
			set_suc = True;

		if struct.has_key('ck_delay'):
			myclock['delay'] = struct['ck_delay'];
			struct['result']['msg'] = self.data['mo_ring_type'][0];
			del struct['ck_delay'];
			if struct.has_key('question') and struct['question'] == 'delay':
				del struct['question'];
			set_suc = True;
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			struct['result']['msg'] = self.data['mo_ring_able'][0];
			del struct['ck_able'];
			if struct.has_key('question') and struct['question'] == 'able':
				del struct['question'];
			set_suc = True;
		if struct.has_key('ck_time'):
			myclock['time'] = struct['ck_time']['time'];
			struct['result']['msg'] = self.data['mo_time_suc'][0];
			del struct['ck_time'];
			if struct.has_key('question') and struct['question'] == 'time':
				del struct['question'];
			set_suc = True;
		if struct.has_key('ck_bell'):
			myclock['bell'] = struct['ck_bell'];
			struct['result']['msg'] = self.data['mo_ring_bell'][0];
			del struct['ck_bell'];
			if struct.has_key('question') and struct['question'] == 'bell':
				del struct['question'];
			set_suc = True;
		if set_suc == False:
			struct['result']['msg'] = self.data['mo_help'][0];
			struct['result']['extra'] = self.data['mo_helpe'][0];
			struct['code'] = 'wait';
		else:
			struct['code'] = 'success';

	def _analysis_clock(self,struct,super_b):
		if not struct.has_key('question'): return None;
		if struct['question'] == 'delay':
			struct['result']['msg'] = self.data['help_delay'][0];
			struct['code'] = 'wait';
		elif struct['question'] == 'bell':
			struct['result']['msg'] = self.data['help_bell'][0];
			struct['code'] = 'wait';
		elif struct['question'] == 'able':
			struct['result']['msg'] = self.data['help_able'][0];
			struct['code'] = 'wait';
		elif struct['question'] == 'time':
			struct['result']['msg'] = self.data['help_time'][0];
			struct['code'] = 'wait';

