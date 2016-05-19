#!/usr/bin/python
#-*- coding : utf-8 -*-
#
import sys,os

import tornado.ioloop
import tornado.web
from webpy import *
from mager import Mager
from result import ResultHandler

class Application(tornado.web.Application):
	def __init__(self):
		self.mager = Mager();
		handlers = [
			(r"/result",ResultHandler(self.mager));
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
