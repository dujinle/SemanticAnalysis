#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler
#=============================================================
abspath = os.path.abspath(__file__);
base_path = os.path.split(abspath)[0];
#============================================================


logfile = base_path + '/../logs/myapp.log';
logging.basicConfig(level=logging.DEBUG,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename=logfile,
	filemode='w');


#################################################################################################
logfile = base_path + '/../logs/myapp.log';
Rthandler = RotatingFileHandler(logfile, maxBytes=10*1024*1024,backupCount=5);
Rthandler.setLevel(logging.INFO);
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
logging.getLogger('').addHandler(Rthandler);

#################################################################################################
