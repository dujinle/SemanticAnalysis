#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

#处理 网络购物  场景
class ShopAnaly(SceneBase):

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
					return None;
				elif func == 'buy':
					self._fetch_buy_info(struct,super_b);
					return None;
			elif struct['step'] == 'select':
				if func == 'selected':
					self._set_express(struct,super_b);
					struct['step'] = 'set_exp';
					return None;
			elif struct['step'] == 'set_exp':
				if func == 'express':
					self._express_service(struct,super_b);
			elif struct['step'] == 'set_pname':
				self._fetch_buy_info(struct,super_b);
				return None;
			elif struct['step'] == 'set_pnum':
				self._fetch_buy_info(struct,super_b);
				return None;
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _get_shop_info(self,struct,super_b):
		ComFuncs._set_msg(struct,self.data['msg']['shop_info']);
		return None;

	def _search_shop_info(self,struct,super_b):
		nlist = list();
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('type') and item['type'] == 'NB':
				nlist.append(item['str']);
			elif item.has_key('type') and item['type'] == 'N':
				nlist.append(item['str']);
		if len(nlist) <= 0:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
			struct['step'] = 'end';
			return None;
		else:
			shop = super_b.get_shop_info(nlist);
			struct['step'] = 'select';
			ComFuncs._set_msg(struct,self.data['msg']['product_info']);
		return None;

	def _select_succ(self,struct,super_b):
		ComFuncs._set_msg(struct,self.data['msg']['express_sel']);

	def _express_service(self,struct,super_b):
		poi = None;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('type') and item['type'] == 'NPI':
				poi = item['str'];
		if poi is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['expr'] = poi;
			ComFuncs._set_msg(struct,self.data['msg']['express_ser']);

	def __fetch_buy_info(self,struct,super_b):
		self._set_buy_info(struct,super_b);
		self._check_buy_info(struct,super_b);

	def _set_buy_info(self,struct,super_b):
		if super_b.product is None: super_b.product = dict();
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('type') and item['type'] == 'N':
				super_b.product['name'] = item['str'];
			elif item.has_key('type') and item['type'] == 'NUNIT':
				super_b.product['num'] = item['str'];

	def _check_buy_info(self,struct,super_b):
		if super_b.product is None:
			ComFuncs._set_msg(struct,self.data['msg']['set_pname']);
			struct['step'] = 'set_pname';
			return None;
		elif not super_b.product.has_key('name'):
			ComFuncs._set_msg(struct,self.data['msg']['set_pname']);
			struct['step'] = 'set_pname';
			return None;
		elif not super_b.product.has_key('num'):
			ComFuncs._set_msg(struct,self.data['msg']['set_pnum']);
			struct['step'] = 'set_pnum';
			return None;
		else:
			struct['result']['product'] = super_b.product;
			struct['step'] = 'end';
			ComFuncs._set_msg(struct,self.data['msg']['buy_ser']);
