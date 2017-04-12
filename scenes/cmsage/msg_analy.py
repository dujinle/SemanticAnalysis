#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

#处理 电话短信  场景
class MsgAnaly(SceneBase):
	def encode(self,struct,super_b):
		try:
			logging.info('go into message analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				self._send_message(struct,super_b);
				return None;
			elif struct['step'] == 'set_user':
				self._send_message(struct,super_b);
				return None;
			elif struct['step'] == 'set_info':
				self._send_message(struct,super_b);
				return None;
			elif struct['step'] == 'ifread':
				ret = self._read_msg(struct,super_b);
				if ret == True: return None;
			elif struct['step'] == 'reply':
				ret = self._reply_msg(struct,super_b);
				if ret == True: return None;
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _read_msg(self,struct,super_b):
		read = 0;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'READ':
				read = read | 1;
			if item.has_key('stype') and item['stype'] == 'NO':
				read = read | (1 << 1);
		if read > 1 or read == 0:
			struct['result']['status'] = 'filter';
			return False;
		else:
			info = super_b.get_message();
			ComFuncs._set_msg(struct,self.data['msg']['read_message'],info);
			struct['step'] = 'reply';
			return True;

	def _reply_msg(self,struct,super_b):
		reply = 0;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'REPLY':
				reply = reply | 1;
			if item.has_key('stype') and item['stype'] == 'NO':
				reply = reply | (1 << 1);
			if item.has_key('stype') and item['stype'] == 'NOTHING':
				reply = reply | (1 << 1);
		if reply > 1 or reply == 0:
			struct['result']['status'] = 'filter';
			return False;
		else:
			struct['result']['status'] = 'reply';
			struct['step'] = 'send';
			return True;

	def _send_message(self,struct,super_b):
		self._fetch_user(struct,super_b);
		self._fetch_info(struct,super_b);
		self._check_msg(struct,super_b);

	def _check_msg(self,struct,super_b):
		if super_b.msg is None:
			ComFuncs._set_msg(struct,self.data['msg']['unk_user']);
			struct['step'] = 'set_user';
			return None;
		if not super_b.msg.has_key('user'):
			ComFuncs._set_msg(struct,self.data['msg']['unk_user']);
			struct['step'] = 'set_user';
			return None;
		if not super_b.msg.has_key('info'):
			ComFuncs._set_msg(struct,self.data['msg']['unk_info']);
			struct['step'] = 'set_info';
			return None;
		ComFuncs._set_msg(struct,self.data['msg']['send_message']);
		struct['result']['msg'] = super_b.msg;
		struct['step'] = 'end';

	def _fetch_info(self,struct,super_b):
		if super_b.msg is None: super_b.msg = dict();

		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'CONTENT':
				tstr = item['str'];
				sid = struct['text'].find(tstr);
				super_b.msg['info'] = struct['text'][sid:];

	def _fetch_user(self,struct,super_b):
		if super_b.msg is None: super_b.msg = dict();

		p_u = False;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'GIVE':
				p_u = True;
			if item.has_key('type') and item['type'] == 'NB':
				if p_u == True:
					super_b.msg['user'] = item['str'];
					break;
			elif item.has_key('type') and item['type'] == 'RP':
				if p_u == True:
					super_b.msg['user'] = item['str'];
					break;

