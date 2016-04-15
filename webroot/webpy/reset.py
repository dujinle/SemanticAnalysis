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

class ResetHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('type'):
				self.except_handle('the url data format error');
				return ;
			dtype = self.body_json['type'];
			if len(dtype) == 0:
				self.except_handle('the param type is empty');
				return ;
			logging.info('the load data type:[%s]' %dtype);
			mager = self.get_mager();
			sres = mager.reset(dtype);
			self.write(self.gen_result(0,'reset data type:[' + dtype + '] + success',None));
		except Exception as e:
			self.except_handle('reset data type failed');
			return;
