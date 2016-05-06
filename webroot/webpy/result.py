#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
#=============================================
''' import common module '''
base_path = os.path.dirname(__file__);
sys.path.append(base_path + '/../../commons');
#=============================================

import tornado.web
from logger import *
import common
from handler import RequestHandler
from myexception import MyException

class ResultHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('text'):
				self.except_handle('the url data format error');
				return ;
			if not self.body_json.has_key('mdl'):
				self.except_handle('not found argumen mdl');
				return ;
			mdl = self.body_json['mdl'];
			itest = self.body_json['text'];
			if len(itest) == 0:
				self.except_handle('the param text is empty');
				return ;
			logging.info('mdl:%s input:%s' %(mdl,itest));
			mager = self.get_mager();
			sres = mager.encode(itest,mdl);
			ret = dict();
			ret['text'] = sres['text'];
			ret['inlist'] = sres['inlist'];
			ret['value'] = sres['value'];
			ret['dir'] = sres['dir'];
			self.write(self.gen_result(0,'enjoy success',ret));
		except MyException as e:
			self.except_handle(e.value);
			return;
