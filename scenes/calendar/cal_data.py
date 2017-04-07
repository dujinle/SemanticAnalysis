#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from scene_base import SceneBase

class CalData(SceneBase):

	def get_time_info(self,date):
		return self.data['date'];
