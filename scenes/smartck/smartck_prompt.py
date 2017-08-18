#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from myexception import MyException
from common import logging
import com_funcs as SceneParam
import smartck_common as SmartckCom

from scene_base import SceneBase
#闹铃提示方式设置
class SmartckPrompt(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm prompt......');
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_prompt': return None;
			if super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				struct['step'] = 'end';
				return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				self._set_clock_prompt(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _set_clock_prompt(self,struct,super_b):
		myclock = super_b.myclock;
		ms = self._get_match_info(struct['ttag']);
		if ms is None: return None;
		if ms['func'] == 'once':
			myclock['prompt'] = dict();
			myclock['prompt']['type'] = 'once';
		elif ms['func'] == 'last':
			myclock['prompt'] = dict();
			myclock['prompt']['type'] = 'last';
		else:
			SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
			return None;
		SceneParam._set_msg(struct,self.data['msg']['set_prompt_succ']);

	def _get_match_info(self,ttag):
		for temp in self.data['template']:
			comp = re.compile(temp['reg']);
			match = comp.search(ttag);
			if not match is None: return temp;
		return None;
