#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from com_base import ComBase as ShopBase
import com_funcs as ComFuncs

#处理 网络购物  场景
class ShopAnalysis(ShopBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into Shop analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			print 'func:' + func
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

	def _get_shop_info(self,struct,super_b):
		ComFuncs._set_msg(struct,self.data['msg']['shop_info']);
		return None;

	def _search_shop_info(self,struct,super_b):
		sth = sb = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			while True:
				if item['type'] == 'STH' or item['type'] == 'SABST':
					sth = item['str'];
					if item.has_key('belong'):
						if item['belong']['type'] == 'SB':
							sb = item['belong']['str'];
				if item['type'] == 'SB':
					sb = item['str'];
				if item.has_key('child'): item = item['child'];
				else: break;
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
