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
class AlarmSearch():

	def encode(self,struct,super_b):
		try:
			ept = 0;
			print 'go into search module';
			for ck in struct['clocks']:
				if ck['type'] == 'all':
					ept = 1;
					break;
			if ept == 1:
				struct['result'] = super_b.clocks;
			elif struct.has_key('ck_name') and struct['ck_name'] <> 'null':
				if not super_b.myclock is None:
					struct['result'] = super_b.myclock;
				else:
					struct['result'] = 'no found the alarm';
			else:
				struct['result'] = super_b.clocks;
		except Exception as e:
			raise MyException(format(e));
