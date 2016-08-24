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
import pgsql
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
from alarm_help import AlarmHelp

class AEngin():

	def __init__(self):
		self.clocks = dict();
		self.prev_ck = None;
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
		self.alarm_help = AlarmHelp();
		self.p_conn = pgsql.pg_conncet();

	def init(self,fdir):
		self.alarm_add.load_data(fdir + '/message.txt');
		self.alarm_del.load_data(fdir + '/message.txt');
		self.alarm_open.load_data(fdir + '/message.txt');
		self.alarm_off.load_data(fdir + '/message.txt');
		self.alarm_help.load_data(fdir + '/message.txt');
		self.alarm_modify.load_data(fdir + '/message.txt');
		self.alarm_encode.load_data(fdir + '/adjust.txt');

	def _init(self,struct):
		if struct.has_key('clocks'): del struct['clocks'];
		if struct.has_key('ck_action'): del struct['ck_action'];
		if struct.has_key('ck_name'): del struct['ck_name'];
		if struct.has_key('result'): struct['result'] = dict();
		if struct.has_key('code'): del struct['code'];

	def encode(self,struct):
		try:
			self._init(struct);
			print 'alarm init succ';
			self.alarm_encode.encode(struct);
			print 'alarm encode succ';
			self.alarm_fname.encode(struct);
			print 'alarm find name succ';
			if self.action == 'add':
				self.alarm_add.encode(struct,self);
				if struct.has_key('code') and struct['code'] == 'success':
					self._add_alarm2clocks(struct);
					self.prev_ck = self.myclock;
					self.action = self.myclock = None;

			self._find_action(struct);
			print 'find action succ';
			if struct.has_key('ck_action') and struct['ck_action'] == 'add' and self.action <> 'add':
				self.myclock = None;
				self.alarm_add.encode(struct,self);
				if struct.has_key('code'):
					if struct['code'] == 'success':
						self._add_alarm2clocks(struct);
						self.prev_ck = self.myclock;
						self.action = None;
					elif struct['code'] <> 'error':
						self.action = 'add';
				else:
					self.action = 'add';

			if (struct.has_key('ck_action') and struct['ck_action'] == 'modify') or self.action == 'modify':
				if struct.has_key('ck_name') and struct['ck_name'] <> '': self.myclock = self._find_myclock(struct,True);
				self.alarm_modify.encode(struct,self);
				if struct.has_key('code') and struct['code'] == 'wait':
					self.action = 'modify';
				else:
					self.action = None;
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'del') or self.action == 'del':
				self.myclock = self._find_myclock(struct,True);
				self.alarm_del.encode(struct,self);
				self.action = None;
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'search') or self.action == 'search':
				self.myclock = self._find_myclock(struct,False);
				if self.myclock is None: self.myclock = self.prev_ck;
				self.alarm_search.encode(struct,self);
				self.action = None;
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'off'):
				self.myclock = self._find_myclock(struct,True);
				if self.myclock is None: self.myclock = self.prev_ck;
				self.alarm_off.encode(struct,self);
			elif (struct.has_key('ck_action') and struct['ck_action'] == 'open'):
				self._find_myclock(struct,True);
				if self.myclock is None: self.myclock = self.prev_ck;
				self.alarm_open.encode(struct,self);
			elif (struct.has_key('ck_action') and struct['ck_action'].find('help') <> -1):
				self.alarm_help.encode(struct,self);
		except Exception as e:
			raise MyException(format(e));

	def _find_myclock(self,struct,del_tag):
		if not struct.has_key('ck_name'): return None;
		for ck in self.clocks.keys():
			clock = self.clocks[ck];
			if struct['ck_name'] == clock['time'] or (clock.has_key('name') and struct['ck_name'] == clock['name']):
				if del_tag == True: del struct['ck_name'];
				return clock;

	def _add_alarm2clocks(self,struct):
		if self.myclock.has_key('name'):
			self.clocks[self.myclock['name']] = self.myclock;
			struct['result']['clock'] = dict(self.myclock);
		else:
			self.clocks[self.myclock['time']] = self.myclock;
			struct['result']['clock'] = dict(self.myclock);


	#find this action [add del modify search other]
	#|have|what|open|close|clock|no|ring|how|#
	def _find_action(self,struct):
		tag = 0;
		fclock = self._find_myclock(struct,False);
		for ck in struct['clocks']:
			if ck['type'] == 'add':
				struct['ck_action'] = 'add';
				break;
			elif ck['type'] == 'set':
				if fclock is None: struct['ck_action'] = 'add';
				else: struct['ck_action'] = 'modify';
				break;
			elif ck['type'] == 'modify':
				struct['ck_action'] = 'modify';
				break;
			elif ck['type'] == 'del':
				struct['ck_action'] = 'del';
				break;
			elif ck['type'] == 'search':
				struct['ck_action'] = 'search';
				break;
			elif ck['type'] == 'off':
				struct['ck_action'] = 'off';
				break;
			elif ck['type'] == 'open':
				struct['ck_action'] = 'open';
				break;
			elif ck['type'] == 'no': tag = tag | (1 << 2);
			elif ck['type'] == 'ring': tag = tag | (1 << 1);
			elif ck['type'] == 'clock': tag = tag | (1 << 3);
			elif ck['type'] == 'off': tag = tag | (1 << 4);
			elif ck['type'] == 'how': tag = tag | (1);
			elif ck['type'] == 'have': tag = tag | (1 << 7);
			elif ck['type'] == 'what': tag = tag | (1 << 6);
		if tag & 6 == 6: struct['ck_action'] = 'off';
		elif tag & 32 == 32: struct['ck_action'] = 'open';
		elif tag & 10 == 10: struct['ck_action'] = 'open';
		elif tag & 200 == 200: struct['ck_action'] = 'search';
		if tag & 1 == 1 and struct.has_key('ck_action') and struct['ck_action'] == 'add':
			struct['ck_action'] = 'help_add';
		elif tag & 1 == 1 and struct.has_key('ck_action') and struct['ck_action'] == 'modify':
			struct['ck_action'] = 'help_modify';
		elif tag & 1 == 1 and struct.has_key('ck_action') and struct['ck_action'] == 'search':
			struct['ck_action'] = 'help_search';
		elif tag & 1 == 1 and struct.has_key('ck_action') and struct['ck_action'] == 'del':
			struct['ck_action'] = 'help_del';
		elif tag & 1 == 1:
			struct['ck_action'] = 'help_main';

