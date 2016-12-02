#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from shop_base import ShopBase
import com_funcs as ComFuncs

#处理 电话短信  场景
class ShopAnalysis(ShopBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into Shop analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			print func
			if struct['step'] == 'start':
				if func == 'shop':
					self._get_shop_info(struct,super_b);
				elif func == 'search':
					self._search_shop_info(struct,super_b);
					struct['step'] = 'select';
					return None;
				elif func == 'buy':
					self._get_buy_info(struct,super_b);
			elif struct['step'] == 'select':
				if func == 'selected':
					self._select_succ(struct,super_b);
					struct['step'] = 'express';
					return None;
			elif struct['step'] == 'express':
				if func == 'express':
					self._express_service(struct,super_b);
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
			elif item.has_key('status'): reg = reg + item['status']['stype'];
		print 'reg:' + reg
		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

	def _get_shop_info(self,struct,super_b):
		ComFuncs._set_msg(struct,self.data['msg']['shop_info']);
		return None;

	def _search_shop_info(self,struct,super_b):
		sth = sb = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['type'] == 'STH' or item['type'] == 'SABST':
				sth = item['str'];
				if item.has_key('child'):
					if item['child']['type'] == 'SB':
						sb = item['child']['str'];
			if item['type'] == 'SB':
				sb = item['str'];
			del struct[istr]
		if sth is None and sb is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
			return None;
		else:
			shop = super_b.get_shop_info(sth,sb);
			ComFuncs._set_msg(struct,self.data['msg']['baby_info']);
		return None;

	def _select_succ(self,struct,super_b):
		ComFuncs._set_msg(struct,self.data['msg']['express_sel']);

	def _express_service(self,struct,super_b):
		ComFuncs._set_msg(struct,self.data['msg']['express_ser']);

	def _get_buy_info(self,struct,super_b):
		ComFuncs._set_msg(struct,self.data['msg']['buy_ser']);
