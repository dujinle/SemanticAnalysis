#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
import tornado.web

#=============================================
''' import common module '''
base_path = os.path.dirname(__file__);
sys.path.append(base_path + '/../../commons');
#=============================================

from logger import *
import common
from handler import RequestHandler

class GetHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('type'):
				self.except_handle('the url data format error');
				return ;
			ctype = self.body_json['type'];
			mager = self.get_mager();
			logging.info('get data: type:' + ctype);
			rest = mager.deal_data(ctype,'get',None);
			print rest;
			self.write(self.gen_result(0,ctype + ' get words success',rest));
		except Exception,e:
			self.except_handle('get ' + ctype + ' failed');
			return ;
