#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil
class MarkDist():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			print 'go into markdist.......';
			self._dist_scene(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _dist_scene(self,struct):
		scenes = dict();
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item.has_key('scene'):
				scenes[item['scene']] = item['stype'];
			if item.has_key('parent'):
				parent = item['parent'];
				if parent.has_key('scene'):
					scenes[parent['scene']] = parent['stype'];
				reg = reg + parent['stype'];
			reg = reg + item['stype'];
			if item.has_key('child'):
				child = item['child'];
				if child.has_key('scene'):
					scenes[child['scene']] = child['stype'];
				reg = reg + child['stype'];

		for scene in self.data.keys():
			item = self.data[scene];
			print item['reg'],reg;
			comp = re.compile(item['reg']);
			match = comp.search(reg);
			if match is None : continue;
			scenes[scene] = reg;
		if len(scenes) > 0:
			scene = scenes.keys()[0];
			ilen = scenes[scene];
			for sc in scenes.keys():
				item = scenes[sc];
				if len(item) > len(ilen):
					ilen = item;
					scene = sc;
			struct['scene'] = scene;
