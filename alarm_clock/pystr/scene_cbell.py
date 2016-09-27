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
from common import logging

from base import Base
#修改铃声场景设置
class SceneCBell(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm bell');
			if super_b.myclock is None:
				struct['result']['msg'] = self.data['msg']['ck_unknow'][0];
				struct['code'] = 'exit';
				return None;
			if not sturct.has_key('step'): sturct['step'] = 'start';

			if struct['step'] == 'start':
				struct['result']['msg'] = self.data['msg']['set_start'];
				#self.send_msg(struct);
				#开始参数设置向导
				struct['result']['msg'] = self.data['msg']['set_bell_type'][0];
				struct['step'] = 'set_bell_type';
			elif struct['step'] == 'set_bell_type':
				btype = self._set_bell_type(struct,super_b);
				struct['step'] = 'select_which_bell';
				if btype == 'ring':
					struct['result']['msg'] = self.data['msg']['raise_ring'];
				elif btype == 'music':
					struct['result']['msg'] = self.data['msg']['raise_music'];
			elif struct['step'] == 'select_which_bell':
				self._make_sure_bell(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _set_bell_type(self,struct,super_b):
		myclock = super_b.myclock;
		if not myclock.has_key('bell'): myclock['bell'] = dict();

		for ck in struct['clocks']:
			if ck['type'] == '_music':
				myclock['bell']['type'] = 'music';
				break;
			elif ck['type'] == '_bell':
				myclock['bell']['type'] = 'ring';
				break;
		if not myclock['bell'].has_key('type'):
			myclock['bell']['type'] = 'ring';
			struct['result']['msg'] = self.data['msg']['type_unknow'][0];
			self.send_msg(struct);
		return myclock['bell']['type'];

	def _make_sure_bell(self,struct,super_b):
		myclock = super_b.myclock;
		for ck in struct['clocks']:
			if ck['type'] == '_yes':
				myclock['bell']['name'] = 'bird';
				myclock['bell']['addr'] = 'bird.mp3';
				break;
		if not myclock['bell'].has_key('name'):
			myclock['bell']['name'] = 'bird';
			myclock['bell']['addr'] = 'bird.mp3';
			struct['result']['msg'] = self.data['msg']['no_bell_sure'][0];
		else:
			struct['result']['msg'] = self.data['msg']['set_bell_succ'][0];
