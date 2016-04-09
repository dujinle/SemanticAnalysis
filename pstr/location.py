#!/usr/bin/python
#-*- coding:utf-8 -*-
from common import *
# load the location info.

class Location:

	def __init__(self):
		self.local = None;

	def load(self,lfile):
		try:
			self.local = load_json(lfile);
		except Exception, e:
			raise e;

	def decode(self,struct):
		inlist = struct['inlist'];
		if not struct.has_key('scene'):
			return None;
		scene = strcut['scene'];
		local = self.toolbox[struct['tool']];
		attr = tool[u'属性'];
		if struct['attr'] in attr:
			if not struct.has_key('api'):
				struct['api'] = [];
			struct['api'].append(attr[struct['attr']]);
			if struct.has_key('direct') and struct.has_key('value'):
				action = tool[u'动作'];
				for ac in action:
					if ac.find(struct['attr']) <> -1:
						struct['api'].append(action[ac]);
		return 'OK';

