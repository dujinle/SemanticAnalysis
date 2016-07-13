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
from alarm_add import AlarmAdd
from alarm_del import AlarmDel
from alarm_encode import AlarmEncode
from alarm_modify import AlarmModify

class AEngin():

	def __init__(self):
		self.clocks = dict();
		self.myclock = None;
		self.action = None;
		self.alarm_encode = AlarmEncode();
		self.alarm_modify = AlarmModify();
		self.alarm_add = AlarmAdd();
		self.alarm_del = AlarmDel();

	def init(self):
		self.alarm_add.load_data('./tdata/message.txt');
		self.alarm_encode.load_data('./tdata/adjust.txt');

	def encode(self,struct):
		try:
			if struct.has_key('result'): del struct['result'];
			self.alarm_encode.encode(struct);
			self._find_myclock(struct);
			if self.action == 'add' or (struct.has_key('ck_action') and struct['ck_action'] == 'add'):
				self.alarm_add.encode(struct,self);
				self.action = 'add';
				if struct.has_key('code') and struct['code'] == 'success':
					self.action = None;
			elif self.action == 'modify':
				self.alarm_modify.encode(struct,self);
				self.action = None;
			elif self.action == 'del':
				self.alarm_del.encode(struct,self);
				self.action = None;
		except Exception as e:
			raise MyException(format(e));

	def _find_myclock(self,struct):
		#if not self.myclock is None: return None;
		if not struct.has_key('ck_name'): return None;
		for ck in self.clocks.keys():
			clock = self.clocks[ck];
			if  struct['ck_name'] == clock['time'] or (struct['ck_name'] in clock['desc']):
				self.myclock = clock;
				break;
		del struct['ck_name'];

