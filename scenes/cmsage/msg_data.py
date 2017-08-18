#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from scene_base import SceneBase

class MsgData(SceneBase):
	def __init__(self):
		self.data = None;
		self.msg = None;

	def get_msg_by_name(self,owner):
		pass;

	def get_message(self):
		return self.data['Message'];
