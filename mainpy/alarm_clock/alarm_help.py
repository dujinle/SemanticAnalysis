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
class AlarmHelp(Base):

	def encode(self,struct,super_b):
		try:
			print 'go into alarm help action';
			if struct['ck_action'] == 'help_main':
				struct['result']['msg'] = self.data['help_main'][0];
				struct['result']['extra'] = self.data['help_maine'][0];
			if struct['ck_action'] == 'help_add':
				struct['result']['msg'] = self.data['help_main'][0];
				struct['result']['extra'] = self.data['help_adde'][0];
			if struct['ck_action'] == 'help_modify':
				struct['result']['msg'] = self.data['help_main'][0];
				struct['result']['extra'] = self.data['help_modifye'][0];
			if struct['ck_action'] == 'help_del':
				struct['result']['msg'] = self.data['help_main'][0];
				struct['result']['extra'] = self.data['help_dele'][0];
			if struct['ck_action'] == 'help_search':
				struct['result']['msg'] = self.data['help_main'][0];
				struct['result']['extra'] = self.data['help_searche'][0];
		except Exception as e:
			raise MyException(format(e));
