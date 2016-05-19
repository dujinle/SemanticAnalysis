#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from phone_base import PhoneBase

class PhoneData(PhoneBase):

	def get_phone_by_name(self,owner):
		if self.data.has_key(owner):
			return self.data[owner];
		return None;
