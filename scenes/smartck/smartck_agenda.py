#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re
import common,math
from common import logging
from myexception import MyException
from scene_base import SceneBase
import smartck_common as SmartckCom
import com_funcs as SceneParam

#新增日程闹钟 或者带有时间的
class SmartckAgenda(SceneBase):

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_agenda_add': return None;

			print 'go into scene agenda......';
			SmartckCom._fetch_time(struct);
			SmartckCom._calc_able(struct);
			if not struct.has_key('step'): struct['step'] = 'start';
			if struct['step'] == 'start':
				super_b.myclock = dict();
				self._set_agenda_info(struct,super_b);
				return None;
			elif struct['step'] == 'trans':
				self._set_clock_info(struct,super_b);
			elif struct['step'] == 'set_time':
				self._set_agenda_info(struct,super_b);
				return None;
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _set_clock_info(self,struct,super_b):
		if super_b.myclock.has_key('name'):
			super_b.myclock['key'] = super_b.myclock['name'];
			super_b.clocks[super_b.myclock['key']] = super_b.myclock;
			SceneParam._set_msg(struct,self.data['msg']['set_succ'],super_b.myclock['name']);
		elif super_b.myclock.has_key('info'):
			super_b.clocks[super_b.myclock['info']] = super_b.myclock;
			super_b.myclock['key'] = super_b.myclock['info'];
			SceneParam._set_msg(struct,self.data['msg']['set_succ'],super_b.myclock['info']);
		else:
			super_b.clocks[super_b.myclock['time']] = super_b.myclock;
			super_b.myclock['key'] = super_b.myclock['time'];
			SceneParam._set_msg(struct,self.data['msg']['set_succ']);

	def _set_agenda_info(self,struct,super_b):
		self._set_time(struct,super_b);
		self._set_name(struct,super_b);
		self._set_able(struct,super_b);
		self._check_param(struct,super_b);
		common.print_dic(super_b.myclock);

	def _set_time(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			myclock['type'] = 'agenda';
			#时间设置完成回应信息
			myclock['time'] = struct['ck_time']['time'];
			del struct['ck_time'];

	def _set_able(self,struct,super_b):
		myclock = super_b.myclock
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
		else:
			myclock['able'] = dict();
			myclock['able']['type'] = 'week';
			myclock['able']['able'] = '127';

	def _set_name(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_name'):
			myclock['name'] = struct['ck_name'];
			del struct['ck_name'];

	def _check_param(self,struct,super_b):
		if not super_b.myclock.has_key('time'):
			SceneParam._set_msg(struct,self.data['msg']['set_time']);
			struct['step'] = 'set_time';
		else:
			self._set_clock_info(struct,super_b);
			struct['step'] = 'end';

