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

class DelHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('type'):
				self.except_handle('the url data format error');
				return ;
			ctype = self.body_json['type'];
			data = self.body_json['value'];
			logging.info(ctype + ' del words:' + data);
			mager = self.get_mager();
			mager.deal_data(ctype,'del',self.body_json);
			self.write(self.gen_result(0,ctype + ' del words:' + data + ' success',None));
		except Exception,e:
			self.except_handle(format(e));
			return ;
