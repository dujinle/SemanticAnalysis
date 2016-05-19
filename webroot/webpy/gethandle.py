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
				self.except_handle('not found argument type');
				return ;
			if not self.body_json.has_key('mdl'):
				self.except_handle('not found module type');
				return ;
			mdl = self.body_json['mdl'];
			ctype = self.body_json['type'];
			mager = self.get_mager();
			logging.info('get info ' + mdl + ' ' + ctype);
			rest = mager.deal_data(mdl,ctype,'get',None);
			self.write(self.gen_result(0,ctype + ' get words success',rest));
		except Exception,e:
			self.except_handle('get ' + ctype + ' failed');
			return ;
