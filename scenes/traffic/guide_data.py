#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
from common import logging
from myexception import MyException
from scene_base import SceneBase

#处理出行场景
class GuideData(SceneBase):

	#根据起始终点 查找 轨迹数据
	def get_guide(self,start,end):
		for guide in self.data:
			if guide['start'] == start and guide['end'] == end:
				return guide;
		return None;
