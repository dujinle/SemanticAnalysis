#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys
#####################################
sys.path.append('../mainpy');
sys.path.append('../commons');
#####################################

import tornado.web
from logger import *
import common
from handler import RequestHandler
from mager import Mager

class ResultHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('text'):
				self.execpte_handle('the url data format error');
				return ;
			itest = self.body_json['text'];
			if len(itest) == 0:
				self.execpt_handle('the param text is empty');
				return ;
			logging.info('input:%s' %itest);
			sres = self.menj.encode(itest);
			ret = dict();
			ret['text'] = sres['text'];
			ret['inlist'] = sres['inlist'];
			ret['value'] = sres['value'];
			ret['dir'] = sres['dir'];
			self.write(self.gen_result(0,'enjoy success',ret));
		except Exception as e:
			self.execpt_handle(format(e));
			return;
