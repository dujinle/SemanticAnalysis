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
from alarm_search import AlarmSearch
from alarm_modify import AlarmModify
from alarm_fname import AlarmFname
from alarm_off import AlarmOff
from alarm_open import AlarmOpen

class AEngin():

	def __init__(self):
		self.clocks = dict();
		self.myclock = None;
		self.action = None;
		self.alarm_encode = AlarmEncode();
		self.alarm_modify = AlarmModify();
		self.alarm_add = AlarmAdd();
		self.alarm_del = AlarmDel();
		self.alarm_search = AlarmSearch();
		self.alarm_fname = AlarmFname();
		self.alarm_off = AlarmOff();
		self.alarm_open = AlarmOpen();

	def init(self,fdir):
		self.alarm_add.load_data(fdir + '/message.txt');
		self.alarm_encode.load_data(fdir + '/adjust.txt');

	def encode(self,struct):
		try:
			if struct.has_key('result'): del struct['result'];
			self.alarm_encode.encode(struct);
			self.alarm_fname.encode(struct);
			self._find_myclock(struct);
			if self.action == 'add' or (struct.has_key('ck_action') and struct['ck_action'] == 'add') \
				or (struct.has_key('ck_action') and struct['ck_action'] == 'modify' and self.myclock is None):
				self.alarm_add.encode(struct,self);
				self.action = 'add';
				if struct.has_key('code') and struct['code'] == 'success':
					if self.myclock.has_key('name'):
						self.clocks[self.myclock['name']] = self.myclock;
						struct['result'] = self.myclock;
					else:
						self.clocks[self.myclock['time']] = self.myclock;
						struct['result'] = self.myclock;
					self.action = None;
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'modify') or self.action == 'modify':
				self.alarm_modify.encode(struct,self);
				self.action = None;
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'del') or self.action == 'del':
				self.alarm_del.encode(struct,self);
				self.action = None;
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'search') or self.action == 'search':
				self.alarm_search.encode(struct,self);
				self.action = None;
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'off'):
				self.alarm_off.encode(struct,self);
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'open'):
				self.alarm_open.encode(struct,self);
		except Exception as e:
			raise MyException(format(e));

	def _find_myclock(self,struct):
		#if not self.myclock is None: return None;
		if not struct.has_key('ck_name'): return None;
		for ck in self.clocks.keys():
			clock = self.clocks[ck];
			if struct['ck_name'] == clock['time'] or (clock.has_key('name') and struct['ck_name'] == clock['name']):
				self.myclock = clock;
				break;
		del struct['ck_name'];

