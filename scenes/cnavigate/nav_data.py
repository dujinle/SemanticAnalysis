#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from scene_base import SceneBase

class NavData(SceneBase):
	def __init__(self):
		self.pos = None;
		self.data = None;

	def get_gas_station(self):
		self.pos['poi'] = self.data['GAS'];
