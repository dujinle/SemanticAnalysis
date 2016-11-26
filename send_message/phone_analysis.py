#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from phone_base import PhoneBase
import com_funcs as ComFuncs

#处理 电话短信  场景
class PhoneAnalysis(PhoneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into phone analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'call':
					self._get_call_info(struct,super_b);
				elif func == 'message':
					self._send_message(struct,super_b);
			elif struct['step'] == 'read':
				if func == 'read':
					self._read_message(struct,super_b);
					struct['step'] = 'reply';
					return None;
			elif struct['step'] == 'reply':
				if func == 'no' or func == 'no_reply':
					print 'no reply......';
					pass;
				elif func == 'message':
					self._send_message(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_func(self,struct):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			reg = reg + item['stype'];
			if item.has_key('child'): reg = reg + item['child']['stype'];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

	def _get_call_info(self,struct,super_b):
		owner = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item.has_key('type') and item['type'] == 'STH':
				if item.has_key('BELONGS'):
					belong = item['BELONGS'];
					owner = belong['stype'];
					break;
		if owner is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			phone = super_b.get_phone_by_name(owner);
			if phone is None:
				ComFuncs._set_msg(struct,self.data['msg']['unknow']);
				return None;
			struct['result']['phone'] = phone;
			ComFuncs._set_msg(struct,self.data['msg']['call_succ']);

	def _send_message(self,struct,super_b):
		user = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['type'] == 'SB':
				user = item['stype'];
				break;
			elif item.has_key('child') and item['child']['type'] == 'SB':
				user = item['child']['stype'];
				break;
		if user is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
			return None;
		idx = struct['text'].find(self.data['info']);
		if idx == -1:
			idx = struct['text'].find(self.data['message']);
		if idx == -1:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
			return None;
		tdic = dict();
		tdic['user'] = super_b.get_phone_by_name(user);
		tdic['msg'] = struct['text'][idx:];
		struct['result']['message'] = tdic;
		ComFuncs._set_msg(struct,self.data['msg']['send_message']);

	def _read_message(self,struct,super_b):
		info = super_b.get_message();
		ComFuncs._set_msg(struct,self.data['msg']['read_message'],info);
		return None;


