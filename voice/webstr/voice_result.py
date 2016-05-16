#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
#=============================================
''' import common module '''
base_path = os.path.dirname(__file__);
sys.path.append(base_path + '/../../commons');
sys.path.append(base_path + '/../pystr');
#=============================================

import tornado.web
from logger import *
import common
from handler import RequestHandler
from myexception import MyException
from voice_mager import VoiceMager

smager = None;
class VoiceResultHandler(RequestHandler):

	def __init__(self,*args,**kwargs):
		RequestHandler.__init__(self,*args,**kwargs);
		global smager;
		if smager is None:
			smager = VoiceMager();
			smager.init('Voice');

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
			global smager;
			sres = smager.encode(itest);

			if mdl == 'Voice':
				common.print_dic(sres);
			self.write(self.gen_result(0,'enjoy success',sres));
		except Exception as e:
			logging.info(str(e));
