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
from phone_data import PhoneData
from myexception import MyException
from phone_analysis import PhoneAnalysis
from phone_mkobj import PhoneMkobj
from scene_mager import SceneMager

class PhoneMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','phone_users.txt'),
			os.path.join(base_path,'tdata','under_phone.txt'),
			os.path.join(base_path,'tdata','phone_data.txt')
		];
		self.tag_objs = list();
		self.pdata = PhoneData();
		self.tag_objs.append(PhoneMkobj())
		self.tag_objs.append(PhoneAnalysis());
		self.tag_objs.append(self.pdata);

	def encode(self,struct):
		try:
			print 'go into phone mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.pdata);
		except Exception:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
