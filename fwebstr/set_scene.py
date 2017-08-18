#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
#=============================================
''' import common module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../commons'));
#=============================================

import tornado.web
from logger import *
import common
from handler import RequestHandler
from myexception import MyException

class SetSceneHandler(RequestHandler):

	def __init__(self,*args, **kwargs):
		RequestHandler.__init__(self, *args, **kwargs);

	def initialize(self,mager):
		self.mager = mager;

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('scene'):
				self.except_handle('the url data format error[scene]');
				return ;
			if not self.body_json.has_key('step'):
				self.except_handle('the url data format error[step]');
				return ;
			scene = self.body_json['scene'];
			step = self.body_json['step'];
			if len(step) <> 0 and step <> 'None':
				self.mager.set_step(step);
			if len(scene) <> 0 and scene <> 'None':
				self.mager.set_scene(scene);
			logging.info('set scene:%s step:%s' %(scene,step));
		except Exception as e:
			logging.error(str(e));
			raise e;
