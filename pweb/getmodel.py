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

class GetModelHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		res = None;
		try:
			res = self.menj.get_model();
		except Exception as e:
			logging.error(format(e));
			self.except_handle(format(e));
			return ;
		self.write(self.gen_result(0,'get model success',res));
