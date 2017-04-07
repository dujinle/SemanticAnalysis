#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from scene_base import SceneBase

class PhoneData(SceneBase):
	def __init__(self):
		self.data = None;
		self.user = None;

	def get_phone_by_name(self,owner):
		phones = self.data['Phone'];
		if phones.has_key(owner):
			self.user = phones[owner];
		return self.user;

	def get_message(self):
		return self.data['Message'];
