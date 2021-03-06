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
	def get(self):
		try:
			mager = self.get_mager();
			rest = mager.write_file();
			self.write(self.gen_result(0,'save data success',None));
		except Exception,e:
			self.except_handle('save data failed');
			return ;
