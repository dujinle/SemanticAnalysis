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

class RegSceneHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		if not self.body_json.has_key('word'):
			self.execpte_handle('the url data format error');
			return ;
		itext = self.body_json['word'];
		scate = self.body_json['scene'];
		if len(itext) == 0:
			self.execpt_handle('the param text is empty');
			return ;
		logging.info('%s\tscene:%s itext:%s' %(__file__,scate,itext));
		try:
			self.menj.regscene(scate,itext);
		except Exception,e:
			self.except_handle(format(e));
			return ;
		self.write(self.gen_result(0,'register scene words success',None));
