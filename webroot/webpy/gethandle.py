#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys
#####################################
sys.path.append('../commons');
sys.path.append('../mainpy');
#####################################

import tornado.web
from logger import *
import common
from handler import RequestHandler
#from mager import Mager

class GetHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('cname'):
				self.execpte_handle('the url data format error');
				return ;
			cname = self.body_json['cname'];
			data = self.body_json['value'];
			rest = self.menj.deal_data(cname,'get',None);
			self.write(self.gen_result(0,cname + ' get words success',rest));
		except Exception,e:
			self.except_handle(format(e));
			return ;
