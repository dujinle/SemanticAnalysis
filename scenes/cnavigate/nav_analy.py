#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

class NavAnaly(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into Nav analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'refuel':
					self._get_gas_station(struct,super_b);
				if func == 'visit':
					self._get_visit_info(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _get_gas_station(self,struct,super_b):
		if super_b.pos is None: super_b.pos = dict();

		for strs in struct['stseg']:
			if not struct['stc'].has_key(strs): continue;
			item = struct['stc'][strs];
			if item.has_key('type') and item['type'] == 'NPI':
				super_b.pos['poi'] = item['str'];
			elif item.has_key('type') and item['type'] == 'NP':
				super_b.pos['pos'] = item['str'];
		super_b.get_gas_station();
		struct['result']['pos'] = super_b.pos;
		ComFuncs._set_msg(struct,self.data['msg']['refuel_info']);
		return None;

	def _get_visit_info(self,struct,super_b):
		user = None;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('type') and item['type'] == 'NB':
				user = item;
				break;
		if user is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
			return None;
		else:
			struct['result']['user'] = user;
			ComFuncs._set_msg(struct,self.data['msg']['user_info']);
		return None;
