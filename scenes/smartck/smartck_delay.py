#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
from myexception import MyException
from common import logging
import com_funcs as SceneParam
import smartck_common as SmartckCom

from scene_base import SceneBase
class SmartckDelay(SceneBase):

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_delay': return None;
			logging.info('go into set alarm delay');
			if super_b.myclock is None:
				SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
				struct['code'] = 'exit';
				return None;
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				self._set_clock_delay(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _set_clock_delay(self,struct,super_b):
		myclock = super_b.myclock;
		dtag = self.data['deal_tag'];
		for key in dtag:
			if struct['ttag'].find(key) <> -1:
				tag = dtag[key];
				myclock['status'] = dict(tag);
				myclock['status']['type'] = 'delay';
				break;
		if struct['ttag'].find('_time') <> -1:
			for istr in struct['stseg']:
				if not struct['stc'].has_key(istr): continue;
				item = struct['stc'][istr];
				if item['scope'] == 'min' and item.has_key('num'):
					myclock['status'] = dict();
					myclock['status']['scope'] = 'min';
					myclock['status']['type'] = 'delay';
					myclock['status']['value'] = item['num'];
					break;
		SceneParam._set_msg(struct,self.data['msg']['set_delay_succ']);

