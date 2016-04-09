#!/usr/bin/python
#-*- coding:utf-8 -*-
from common import *

class Scene:
	def __init__(self,redis,sfile):
		self.scene = None;
		try:
			scene = redis.get_data('scene');
			if scene is None:
				self.scene = load_json(sfile);
			else:
				self.scene = json.loads(scene);
		except Exception as e:
			raise e;

	def encode(self,struct):
		if struct.has_key('tool'):
			return 'OK';
		inlist = struct['inlist'];
		scene = self.scene;
		tag = False;
		for it in inlist:
			keys = scene.keys();
			if it in keys:
				struct['scene'] = scene[it];
				tag = True;
				break;
			for key in keys:
				case = scene[key];
				if it in case:
					struct['scene'] = case;
					tag = True;
					break;
			if tag == True:
				break;
		if tag == False:
			return None;
		return 'OK';

	def decode(self,struct):
		inlist = struct['inlist'];
		scene = self.scene;
		for it in inlist:
			keys = scene.keys();
			if it in keys:
				struct['scene'] = scene[it];
				break;
			for key in keys:
				case = scene[key];
				if it in case:
					struct['scene'] = case;
					break;
	def regscene(self,scate,itext):
		if self.scene is None:
			raise ValueError('the scene memery is None');
		if self.scene.has_key(scate):
			item = self.scene[scate];
			if itext in item:
				raise ValueError('the scene has this key word');
			self.scene[scate].append(itext);
		else:
			self.scene[scate] = [];
			self.scene[scate].append(itext);

	def delscene(self,scate,itext):
		if self.scene is None:
			raise ValueError('the scene memery is None');
		if self.scene.has_key(scate):
			item = self.scene[scate];
			if itext in item:
				del item[itext];
	def getscene(self,scate):
		if self.scene is None:
			raise ValueError('the scene memery is None');
		if not self.scene.has_key(scate):
			raise ValueError('the scene has no key[%s]' %scate);
		return self.scene[scate];
