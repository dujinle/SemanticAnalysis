#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,common
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as SceneParam
import smartck_common as SmartckCom

#添加闹钟场景 或者带有时间
class SmartckAdd(SceneBase):

	def encode(self,struct,super_b):
		if not struct.has_key('ck_scene'): return None;
		if struct['ck_scene'] <> 'scene_add': return None;
		try:
			print 'go into scene add action......';
			if not struct.has_key('step'): struct['step'] = 'start';

			SmartckCom._fetch_time(struct);
			SmartckCom._calc_able(struct);
			#启动时响应回复
			if struct['step'] == 'start':
				super_b.myclock = dict();
				#开始设置必须的参数
				self.set_ck_param(struct);
				return None;
			elif struct['step'] == 'set_time':
				self.set_ck_param(struct);
				return None;
			struct['step'] = 'trans';
		except Exception as e:
			raise MyException(sys.exc_info());

	def set_ck_param(self,struct,super_b):
		self._set_time(struct,super_b);
		self._set_name(struct,super_b);
		self._set_able(struct,super_b);
		self._check_param(super_b);

	def _set_time(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			times = struct['ck_time']['time'];
			hour = int(times.split(':')[0]);
			if hour >= self.data['common']['getup_time'][0] \
				and hour <= self.data['common']['getup_time'][1]:
				myclock['type'] = 'getup';
				#时间设置完成回应信息
			else:
				SceneParam._set_msg(self.data['msg']['add_getup_ck']);
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

	def _check_param(self,super_b):
		if not super_b.has_key('ck_time'):
			SceneParam._set_msg(struct,self.data['msg']['set_time']);
			struct['step'] = 'set_time';
		else:
			struct['ck_scene'] = 'ck_getup_add';
			struct['step'] = 'trans';

