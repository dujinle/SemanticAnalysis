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
import common
from myexception import MyException
from common import logging
import scene_param as SceneParam

from scene_base import SceneBase
class SceneBell(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm bell');
			if super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				struct['code'] = 'exit';
				return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				SceneParam._set_msg(struct,self.data['msg']['set_start']);
				#self.send_msg(struct);
				#开始参数设置向导
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

		for ck in struct['clocks']:
			if ck['type'] == '_music':
				myclock['bell']['type'] = 'music';
				break;
			elif ck['type'] == '_bell':
				myclock['bell']['type'] = 'ring';
				break;
		if not myclock['bell'].has_key('type'):
			myclock['bell']['type'] = 'ring';
			#SceneParam._set_msg(struct,self.data['msg']['type_unknow']);
			#self.send_msg(struct);
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
			SceneParam._set_msg(struct,self.data['msg']['no_bell_sure']);
		else:
			SceneParam._set_msg(struct,self.data['msg']['set_bell_succ']);
