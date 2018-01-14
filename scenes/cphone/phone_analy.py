#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

#处理 电话短信  场景
class PhoneAnaly(SceneBase):
	def encode(self,struct,super_b):
		try:
			logging.info('go into phone analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'call':
					self._get_call_info(struct,super_b);
				elif func == 'yuyin':
					self._wired_yuyin(struct,super_b);
			elif struct['step'] == 'recall':
				self._open_call_info(struct,super_b);
			elif struct['step'] == 'ifcall':
				self._open_call_info(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _get_call_info(self,struct,super_b):
		owner = None;
		if not super_b.user is None:
			owner = super_b.user;
		else:
			for istr in struct['stseg']:
				if not struct['stc'].has_key(istr): continue;
				item = struct['stc'][istr];
				if item.has_key('type') and item['type'] == 'NB':
					owner = item;
					break;
				if item.has_key('type') and item['type'] == 'RN':
					owner = item;
					break;
		if owner is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['phone'] = owner;
			if owner["type"] == 'NB':
				ComFuncs._set_msg(struct,self.data['msg']['call_nb_succ']);
			else:
				ComFuncs._set_msg(struct,self.data['msg']['call_rn_succ'],owner["str"]);

	def _wired_yuyin(self,struct,super_b):
		way = user = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['type'] == 'DO':
				if item.has_key('parent'):
					parent = item['parent'];
					if parent.has_key('stype') and parent['stype'] == 'YUYIN':
						if parent.has_key('belong'):
							way = parent['belong'];
							continue;
				if item.has_key('child'):
					child = item['child'];
					if child['type'] == 'SB':
						user = item['child'];
						continue;
			if item['type'] == 'SB':
				user = item;
		if way is None or user is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			super_b.user = user;
			struct['result']['user'] = user;
			struct['result']['way'] = way;
			ComFuncs._set_msg(struct,self.data['msg']['wired_unanswer']);

	def _open_call_info(self,struct,super_b):
		call = None
		handfree = 0;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and \
				(item['stype'] == 'YES' or item['stype'] == 'OK'):
				call = 'call';
				break;
			if item.has_key('stype') and item['stype'] == 'OPEN':
				handfree = 1 | handfree;
			if item.has_key('stype') and item['stype'] == 'HANDFREE':
				handfree = (handfree << 1) | 1;
		if not call is None:
			struct['result']['status'] = 'call';
			if handfree == 3:
				struct['result']['handfree'] = 'open';
			ComFuncs._set_msg(struct,self.data['msg']['call_sure_succ']);
