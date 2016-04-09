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

class RegRegsHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		if not self.body_json.has_key('word'):
			self.execpte_handle('the url data format error');
			return ;
		itext = self.body_json['word'];
		level = self.body_json['level'];
		if len(itext) == 0:
			self.execpt_handle('the param text is empty');
			return ;
		logging.info('%s\tscene:%s itext:%s' %(__file__,level,itext));
		try:
			self.menj.reg_regs(level,itext);
		except Exception,e:
			self.except_handle(format(e));
			return ;
		self.write(self.gen_result(0,'register regs model success',None));
