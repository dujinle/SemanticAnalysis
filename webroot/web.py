#!/usr/bin/python
#-*- coding : utf-8 -*-
#
import sys,os

#---------------------------------------------
''' import webpy module '''
base_path = os.path.dirname(__file__);

sys.path.append(base_path + '/webpy');
#sys.path.append(base_path + '/../commons');
#---------------------------------------------

import tornado.ioloop
import tornado.web
from webpy import *

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/doctor",DocterHandler),
			(r"/get_result",ResultHandler),
			(r"/save_data",SaveHandler),
			(r"/reset",ResetHandler),
			(r"/get",GetHandler),
			(r"/add",AddHandler),
			(r"/del",DelHandler)
		];
		settings = dict(
				template_path = os.path.join(os.path.dirname(__file__),"templates"),
				static_path = os.path.join(os.path.dirname(__file__),"static"),
				debug = True,
		);
		#self.db = conn['demo'];
		tornado.web.Application.__init__(self, handlers, **settings);

class DocterHandler(tornado.web.RequestHandler):
	def post(self):
		self.render('index.html');

	def get(self):
		self.render('index.html');

if __name__=="__main__":

	server = Application();
	server.listen(8082);
	tornado.ioloop.IOLoop.instance().start();
