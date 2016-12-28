#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from com_base import ComBase as CalBase

class CalData(CalBase):

	def get_time_info(self,date):
		return self.data['date'];
