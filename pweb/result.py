#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys
#####################################
sys.path.append('..');
#####################################

import tornado.web
from logger import *
import common
from handler import RequestHandler
from main import MainE

class ResultHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		if not self.body_json.has_key('text'):
			self.execpte_handle('the url data format error');
			return ;
		itest = self.body_json['text'];
		if len(itest) == 0:
			self.execpt_handle('the param text is empty');
			return ;
		logging.info('input:%s' %itest);
		sres = self.menj.enjoy(itest);
		code = sres['code'];
		msg = sres['msg'];
		del sres['msg'];
		del sres['code'];
		self.write(self.gen_result(code,msg,sres));
