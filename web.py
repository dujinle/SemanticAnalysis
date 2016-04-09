#!/usr/bin/python
#-*- coding : utf-8 -*-
#
import sys,os
import tornado.ioloop
import tornado.web
from logger import *
from handler import RequestHandler
from pweb import *
from common import *


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/",ResultHandler),
			(r"/doctor",DocterHandler),
			(r"/get_scene",GetSceneHandler),
			(r"/reg_scene",RegSceneHandler),
			(r"/del_scene",DelSceneHandler),
			(r"/del_word",DelWordHandler),
			(r"/add_word",AddWordHandler),
			(r"/get_dimen",GetDimenHandler),
			(r"/reg_dimen",RegDimenHandler),
			(r"/check_dimen",CheckDimenHandler),
			(r"/get_model",GetModelHandler),
			(r"/reg_regs",RegRegsHandler),
			(r"/reg_quant",RegQuantHandler)
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
