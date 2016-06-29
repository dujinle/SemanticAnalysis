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
			(r"/voice",VoiceHandler),
			(r"/local",LocalHandler),
			(r"/music",MusicHandler),
			(r"/catering",CateringHandler),
			(r"/travel",TravelHandler),
			(r"/temperature",TempHandler),
			(r"/timer",TimerHandler),
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
	def get(self):
		self.render('index.html');

class VoiceHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('voice.html');

class TempHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('temperature.html');
class TimerHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('timer.html');

class LocalHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('local.html');

class MusicHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('music.html');

class CateringHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('catering.html');

class TravelHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('travel.html');

if __name__=="__main__":

	server = Application();
	server.listen(8082);
	tornado.ioloop.IOLoop.instance().start();
