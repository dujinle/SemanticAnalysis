#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
import re,time
from myexception import MyException
from common import logging
import com_funcs as SceneParam
import smartck_common as SmartckCom
from scene_base import SceneBase

class SmartckBell(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm bell');
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_bell': return None;
			if super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				struct['step'] = 'end';
				return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				SceneParam._set_msg(struct,self.data['msg']['set_bell_type']);
				struct['step'] = 'set_bell_type';
			elif struct['step'] == 'set_bell_type':
				btype = self._set_bell_type(struct,super_b);
				struct['step'] = 'select_which_bell';
				if btype == 'ring':
					SceneParam._set_msg(struct,self.data['msg']['raise_ring']);
				elif btype == 'music':
					SceneParam._set_msg(struct,self.data['msg']['raise_music']);
			elif struct['step'] == 'select_which_bell':
				self._make_sure_bell(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _set_bell_type(self,struct,super_b):
		myclock = super_b.myclock;
		if not myclock.has_key('bell'): myclock['bell'] = dict();

		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item['type'] == 'MUSIC':
				myclock['bell']['type'] = 'music';
				break;
			elif item['type'] == 'BELL':
				myclock['bell']['type'] = 'ring';
				break;
		if not myclock['bell'].has_key('type'):
			myclock['bell']['type'] = 'ring';
		return myclock['bell']['type'];

	def _make_sure_bell(self,struct,super_b):
		myclock = super_b.myclock;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item['type'] == 'YES' or item['type'] == 'OK':
				myclock['bell']['name'] = 'bird';
				myclock['bell']['addr'] = 'bird.mp3';
				break;
		if not myclock['bell'].has_key('name'):
			myclock['bell']['name'] = 'bird';
			myclock['bell']['addr'] = 'bird.mp3';
			SceneParam._set_msg(struct,self.data['msg']['no_bell_sure']);
		else:
			SceneParam._set_msg(struct,self.data['msg']['set_bell_succ']);
