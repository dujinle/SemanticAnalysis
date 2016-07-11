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
class AEngin(Base):

	def __init__(self):
		Base.__init__(self);
		self.clocks = dict();
		self.myclock = None;
		self.action = None;

	def encode(self,struct):
		try:
			if struct.has_key('result'): del struct['result'];
			self._find_myclock(struct);
			self._find_action(struct);
			if not struct.has_key('ck_action') and self.action is None:
				struct['result'] = self.data['other'][0];
				self.action = None;
			if self.action == 'add' or (struct.has_key('ck_action') and struct['ck_action'] == 'add'):
				self.action = 'add';
				self._add_clock(struct);
				self._analysis(struct);
			struct['myclock'] = self.myclock;
		except Exception as e:
			raise MyException(format(e));

	def _find_myclock(self,struct):
		if not self.myclock is None: return None;
		if not struct.has_key('ck_name'): return None;
		for ck in self.clocks.keys():
			clock = self.clocks[ck];
			if  struct['ck_name'] == clock['time'] or (struct['ck_name'] in clock['desc']):
				self.myclock = clock;
				break;

	#find this action [add del modify search other]
	def _find_action(self,struct):
		if not struct.has_key('clocks'): return None;
		clocks = struct['clocks'];
		action = None;
		for ck in clocks:
			if ck['type'] == 'add': action = 'add';
			elif ck['type'] == 'del': action = 'del';
			elif ck['type'] == 'search': action = 'search';
			elif ck['type'] == 'set':
				if self.myclock is None: action = 'add';
				else: action = 'modify';
		if not action is None: struct['ck_action'] = action;

	def _add_clock(self,struct):
		if self.myclock is None: self.myclock = dict();
		if struct.has_key('ck_time'):
			ctime = struct['ck_time'];
			if not self.clocks.has_key(ctime['time']):
				self.clocks[ctime['time']] = self.myclock;
			self.myclock['time'] = ctime['time'];
			del struct['ck_time'];
		elif struct.has_key('ck_name') and struct['ck_name'] <> 'null':
			if self.myclock['time'] <> struct['ck_name']:
				self.myclock['desc'].append(struct['ck_name']);
		elif struct.has_key('ck_delay'):
			self.myclock['delay'] = struct['ck_delay'];
			del struct['ck_delay'];
		elif struct.has_key('ck_able'):
			self.myclock['able'] = struct['ck_able'];
			del struct['ck_able'];

	def _analysis(self,struct):
		ck = self.myclock;
		if not ck.has_key('time'):
			struct['result'] = self.data['time'][0];
			return None;
		elif not ck.has_key('delay'):
			struct['result'] = self.data['delay'][0];
			return None;
		elif not ck.has_key('able'):
			struct['result'] = self.data['freq'][0];
			return None;
		struct['result'] = 'add clock success';
		self.action = None;

