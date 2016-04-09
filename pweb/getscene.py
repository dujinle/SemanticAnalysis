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

class GetSceneHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		if not self.body_json.has_key('scene'):
			self.execpte_handle('the url data format error');
			return ;
		scate = self.body_json['scene'];
		if len(scate) == 0:
			self.execpt_handle('the param text is empty');
			return ;
		logging.info('%s\tscene:%s' %(__file__,scate));
		res = None;
		try:
			res = self.menj.getscene(scate);
		except Exception as e:
			logging.error(format(e));
			self.except_handle(format(e));
			return ;
		self.write(self.gen_result(0,'get scene words success',{scate:res}));
