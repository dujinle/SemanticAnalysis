#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,collections
from myexception import MyException
from scene_base import SceneBase

#标记用户列表中的数据
class SmartckData(SceneBase):
	def __init__(self):
		self.clocks = collections.OrderedDict();
		self.myclock = None;

	def get_err_msg(self): return self.data['err_msg'];

	def get_unknow_msg(self): return self.data['msg'];
