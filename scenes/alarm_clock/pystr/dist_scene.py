#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math,datetime
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
from myexception import MyException
from scene_base import SceneBase
import scene_param as SceneParam

#根据模板区分不同的场景
class DistScene(SceneBase):

	def encode(self,struct):
		try:
			tag = '';
			for ck in struct['clocks']:
				if isinstance(ck,dict):
					tag = tag + ck['type'];
			struct['ttag'] = tag;
			self._get_ck_name(struct);
			self._find_scene(tag,struct);
#			common.print_dic(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _find_scene(self,tag,struct):
		for key in self.data.keys():
			calc_key = self.data[key];
			reg_comp = re.compile(calc_key['reg']);
			match = reg_comp.search(tag);
			if match is None: continue;
			struct['ck_reg'] = match.group(0);
			struct['ck_scene'] = key;
			break;
		if struct.has_key('ck_reg'):
			print struct['ck_reg'];
			del struct['ck_reg'];

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
