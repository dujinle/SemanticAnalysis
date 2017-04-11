#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

import common,config
from common import logging
from msg_data import MsgData
from myexception import MyException
from msg_analy import MsgAnaly
from msg_mkuser import MsgMkobj
from scene_mager import SceneMager

class MsgMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','msg_users.txt'),
			os.path.join(base_path,'tdata','under_msg.txt'),
			os.path.join(base_path,'tdata','msg_data.txt')
		];
		self.tag_objs = list();
		self.pdata = MsgData();
		self.tag_objs.append(MsgMkobj())
		self.tag_objs.append(MsgAnaly());
		self.tag_objs.append(self.pdata);

	def encode(self,struct):
		try:
			print 'go into msg mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.pdata);
		except Exception:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
