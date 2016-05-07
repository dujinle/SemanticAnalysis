#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from myexception import MyException
from scene_base import SceneBase
import  smartck_common as SmartckCom

#根据模板区分不同的场景
class SmartckDist(SceneBase):

	def encode(self,struct,super_b): pass;

	def dist_encode(self,struct):
		try:
			func = self._fetch_func(struct);
			print 'dist scene...',func
			if func <> 'None':
				struct['ck_scene'] = func;
			elif struct.has_key('ck_scene'):
				del struct['ck_scene'];
#			self._get_ck_name(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_func(self,struct):
		if not struct.has_key('stc'): return 'None';
		if not struct.has_key('stseg'): return 'None';

		reg = '';
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype'):
				reg = reg + item['stype'];
		struct['ttag'] = reg;

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None:
				return model['type'];
		return 'None';

	def _get_ck_name(self,struct):
		if struct['ttag'].find('WAKE') <> -1:
			struct['ck_name'] = u'起床';
		else:
			name = SmartckCom._find_ck_name(struct);
			if name <> '':
				struct['ck_name'] = name;
			else:
				SmartckCom._fetch_time(struct);
				if struct.has_key('ck_time'):
					tdic = dict();
					tdic['type'] = 'time';
					tdic['name'] = struct['ck_time'];
					struct['ck_tag'] = tdic;

