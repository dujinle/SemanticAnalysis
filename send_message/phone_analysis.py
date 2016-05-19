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
			self._fetch_all_types(struct);

			if struct['step'] == 'start':
				func = self._fetch_func(struct);
				print func
				if func == 'call':
					self._get_call_info(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_all_types(self,struct):
		self._fetch_type(struct,'LocalPrep');
		self._fetch_type(struct,'PerPronom');
		self._fetch_type(struct,'PrepCom');
		self._fetch_type(struct,'VerbCom');

	def _fetch_type(self,struct,key):
		if struct.has_key(key):
			for item in struct[key]: struct[item['str']] = item;
			del struct[key];

	def _fetch_func(self,struct):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			reg = reg + struct[istr]['stype'];

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

