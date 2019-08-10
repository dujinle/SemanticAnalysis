#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
from common import logging
from myexception import MyException
from scene_base import SceneBase as LJFLBase

class LJFLData(LJFLBase):
	def __init__(self):
		LJFLBase.__init__(self);
		self.objs = [];

	def get_message(self):
		return self.data['Message'];
	
	def get_err_msg(self):
		return "";
