#!/usr/bin/python
#-*- coding:utf-8 -*-
import json,os,sys
import tornado.web
import traceback
from logger import *
#==================================================
''' import module mager '''
abspath = os.path.dirname(__file__);

sys.path.append(base_path);
sys.path.append(base_path + '/../mainpy');
#===================================================

from mager import Mager
MAGER = None;

class RequestHandler(tornado.web.RequestHandler):

	mager = None;
	def __init__(self,*args,**kwargs):
		tornado.web.RequestHandler.__init__(self, *args, **kwargs);
		try:
			global MAGER
			if MAGER is None:
				MAGER = Mager();
				MAGER.init('Voice');
				print 'creat menj success ......';
		except Exception as e:
			raise e;

	def get_mager(self):
		global MAGER;
		return MAGER;

	def write(self, trunk):
		if type(trunk) == int:
			trunk = str(trunk);
		super(RequestHandler, self).write(trunk)

	def gen_result(self, code, message, result):
		res = '{ ';
		res += '"code": %s, ' % code;
		res += '"message": "%s' % message;
		if result is None:
			return res + '" }';
		if not isinstance(result, basestring) and type(result) <> int:
			result = json.dumps(result, sort_keys=False,ensure_ascii=False);
			res += '","result": %s' % result;
		return res + ' }';

	def except_handle(self, message):
		s = traceback.format_exc();
		logging.error(s + message);
		msg = message.replace(',',' ').replace('\n','#');
		msg = msg.replace('"',' ');
		msg = msg.replace(';',' ');
		self.write(self.gen_result(-1,msg, None))
		return
