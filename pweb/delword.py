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

class DelWordHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		if not self.body_json.has_key('word'):
			self.execpte_handle('the url data format error');
			return ;
		itext = self.body_json['word'];
		if len(itext) == 0:
			self.except_handle('the param text is empty');
			return ;
		logging.info('%s\tinput:%s' %(__file__,itext));
		try:
			sres = self.menj.del_word(itext);
		except Exception as e:
			self.except_handle(format(e));
			return ;
		self.write(self.gen_result(0,'del word success',None));
