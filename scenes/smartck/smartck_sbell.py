#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
import re,time
from myexception import MyException
from common import logging
import com_funcs as SceneParam
import smartck_common as SmartckCom
from scene_base import SceneBase

#直接设置铃声提示音的场景
class SmartckSBell(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm bell......');
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_sbell': return None;
			if super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				struct['step'] = 'end';
				return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				self._encode_bell(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _encode_bell(self,struct,super_b):
		myclock = super_b.myclock;
		for tm in self.data['rings']:
			if struct['text'].find(tm) <> -1:
				if not myclock.has_key('bell'): myclock['bell'] = dict();
				myclock['bell'].update(self.data['rings'][tm]);
				myclock['bell']['name'] = tm;
				break;
		for tm in self.data['music']:
			if struct['text'].find(tm) <> -1:
				if not myclock.has_key('bell'): myclock['bell'] = dict();
				myclock['bell'].update(self.data['music'][tm]);
				myclock['bell']['name'] = tm;
				break;
		if myclock.has_key('bell') and myclock['bell'].has_key('name'):
			SceneParam._set_msg(struct,self.data['msg']['set_bell_succ']);
		else:
			SceneParam._set_msg(struct,self.data['msg']['bell_unknow']);
