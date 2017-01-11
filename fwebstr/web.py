#!/usr/bin/python
#-*- coding : utf-8 -*-
#
import sys,os
import tornado.ioloop
import tornado.web

base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../'));

from mager import Mager
from result import ResultHandler

class Application(tornado.web.Application):
	def __init__(self):
		self.mager = Mager();
		self.mager.init();
		handlers = [
			(r"/get_sresult",ResultHandler,{'mager':self.mager}),
		];
		settings = dict(
				template_path = os.path.join(os.path.dirname(__file__),"templates"),
				static_path = os.path.join(os.path.dirname(__file__),"static"),
				debug = True,
		);
		tornado.web.Application.__init__(self, handlers, **settings);

if __name__=="__main__":

	server = Application();
	server.listen(8082);
	tornado.ioloop.IOLoop.instance().start();
