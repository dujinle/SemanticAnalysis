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
from set_scene import SetSceneHandler

class Application(tornado.web.Application):
	def __init__(self):
		self.mager = Mager();
		self.mager.init();
		handlers = [
			(r"/get_sresult",ResultHandler,{'mager':self.mager}),
			(r"/set_scene",SetSceneHandler,{'mager':self.mager}),
		];
		settings = dict(
				template_path = os.path.join(os.path.dirname(__file__),"templates"),
				static_path = os.path.join(os.path.dirname(__file__),"static"),
				debug = True,
		);
		tornado.web.Application.__init__(self, handlers, **settings);

if __name__=="__main__":

	port = sys.argv[1];
	server = Application();
	server.listen(port);
	tornado.ioloop.IOLoop.instance().start();
