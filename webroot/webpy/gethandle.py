#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys
#===========================================
''' import commons mainpy module '''
#abspath = os.path.abspath(__file__);
#base_path = os.path.split(abspath)[0];

#sys.path.append(base_path + '/../../commons');
#sys.path.append('../mainpy');
#==========================================

import tornado.web
from logger import *
import common
from handler import RequestHandler
#from mager import Mager

class GetHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('type'):
				self.except_handle('the url data format error');
				return ;
			ctype = self.body_json['type'];
			rest = self.menj.deal_data(ctype,'get',None);
			print rest;
			self.write(self.gen_result(0,ctype + ' get words success',rest));
		except Exception,e:
			self.except_handle('get ' + ctype + ' failed');
			return ;
