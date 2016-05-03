#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from myexception import MyException
from scene_base import SceneBase
import com_funcs as SceneParam

#根据模板区分不同的场景
class SmartckDist(SceneBase):

	def encode(self,struct): pass;

	def dist_encode(self,struct):
		try:
			if not struct.has_key('step'): return None;
			if struct['step'] <> 'end': return None;

			func = self._fetch_func(struct);
			if func <> 'None':
				struct['ck_scene'] = func;
			else:
				if struct.has_key['ck_scene']: del struct['ck_scene'];
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
			if not match is None: return model['func'];
		return 'None';

	def _get_ck_name(self,struct):
		if struct['ttag'].find('_wake') <> -1:
			struct['ck_name'] = u'起床';
		else:
			name = SceneParam._find_ck_name(struct,'_clock');
			if name is None:
				name = SceneParam._find_ck_name(struct,'_remind');
			if name is None:
				name = SceneParam._find_ck_name(struct,'_agenda');
			if not name is None and len(name) > 0:
				struct['ck_name'] = name;
