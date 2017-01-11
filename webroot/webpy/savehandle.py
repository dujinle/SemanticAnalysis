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

class SaveHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('mdl'):
				self.except_handle('not found module type');
				return ;
			mdl = self.body_json['mdl'];
			mager = self.get_mager();
			rest = mager.write_file(mdl);
			self.write(self.gen_result(0,mdl + 'save data success',None));
		except Exception,e:
			self.except_handle(mdl + 'save data failed');
			return ;
