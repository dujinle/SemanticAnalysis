#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys
import tornado.web
from logger import *
import common
from handler import RequestHandler

class AddHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('cname'):
				self.execpte_handle('the url data format error');
				return ;
			cname = self.body_json['cname'];
			data = self.body_json['value'];
			logging.info(cname + ' add words:' + data);
			self.menj.deal_data(cname,'add',self.body_json);
			self.write(self.gen_result(0,cname + ' add words:' + data + ' success',None));
		except Exception,e:
			self.except_handle(format(e));
			return ;
