#!/usr/bin/python
#-*- coding:utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.DEBUG,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='myapp.log',
	filemode='w');


#################################################################################################
Rthandler = RotatingFileHandler('myapp.log', maxBytes=10*1024*1024,backupCount=5);
Rthandler.setLevel(logging.INFO);
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
logging.getLogger('').addHandler(Rthandler);

#################################################################################################
