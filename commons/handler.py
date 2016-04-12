#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
import tornado.web
from logger import logging
from mager import Mager

class RequestHandler(tornado.web.RequestHandler):

	def __init__(self,*args,**kwargs):
		tornado.web.RequestHandler.__init__(self, *args, **kwargs);
		try:
			self.menj = Mager();
			self.menj.init();
		except Exception as e:
			logging.error(format(e));
			raise e;

	def write(self, trunk):
		if type(trunk) == int:
			trunk = str(trunk);
		super(RequestHandler, self).write(trunk)

	def gen_result(self, code, message, result):
		res = '{ ';
		res += '"code": %s, ' % code;
		res += '"message": "%s' % message;
		if result is None:
			logging.info(res);
			return res + '" }';
		if not isinstance(result, basestring) and type(result) <> int:
			result = json.dumps(result, sort_keys=False,ensure_ascii=False);
			res += '","result": %s' % result;
		logging.info(res);
		return res + ' }';

	def except_handle(self, message):
		logging.error(message)
		self.write(self.gen_result(-1, message, None))
		return
