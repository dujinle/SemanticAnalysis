#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase as LJFLBase
import com_funcs as ComFuncs

#处理 垃圾分类  场景
class LJFLAnalysis(LJFLBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into lajifenlei analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			self._merge_objs(struct,super_b);
			self._match_class(struct,super_b);
			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'nothrow':
					self._get_nothrow_info(struct,super_b);
				elif func == 'throw':
					self._get_throw_info(struct,super_b);
				else:
					self._get_unknow_info(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	#对对象进行分类分析，垃圾有很多分类这里比较麻烦 日
	def _match_class(self,struct,super_b):
		for key in self.data['fenlei']:
			item = self.data['fenlei'][key];
			for obj in super_b.objs:
				obj['class'] = 'unknow';
				if obj['type'] != item['type']:
					continue;
				track = stype = '';
				for stc in obj['stc']:
					track += ''.join(stc['track']);
					stype += stc['stype'];
				flag = False;
				for st in item['match']:
					mm = item['match'][st];
					if st == 'track':
						for mstr in mm:
							idx = track.find(mstr);
							if idx == -1:
								continue;
							else:
								obj['class'] = key;
								flag = True;
								break;
					elif st == 'stype':
						for mstr in mm:
							idx = stype.find(mstr);
							if idx == -1:
								continue
							else:
								obj['class'] = key;
								flag = True;
								break;
					if flag == True:break;

	#合并对象
	def _merge_objs(self,struct,super_b):
		final_objs = [];
		for item in super_b.objs:
			dic = {
				'str':'',
				'stype':'',
				'type':'',
				'stc':[]
			};

			for it in item:
				dic['str'] += it['str'];
				dic['stype'] += it['stype'];
				dic['type'] = it['type'];
				dic['stc'].append(it);
			final_objs.append(dic);
		super_b.objs = final_objs;

	def _get_nothrow_info(self,struct,super_b):
		struct['result']['action'] = 'nothrow';
		struct['result']['objs'] = [];
		strs = ''
		for item in super_b.objs:
			it = dict(item);
			del it['stc'];
			struct['result']['objs'].append(it);
			strs += it['str'] + ',';
		if len(strs) >= 2:
			strs = strs[:len(strs) - 1];
		ComFuncs._set_msg(struct,self.data['msg']['nothrow'],strs);

	def _get_throw_info(self,struct,super_b):
		struct['result']['action'] = 'throw';
		struct['result']['objs'] = [];
		strs = ''
		for item in super_b.objs:
			it = dict(item);
			del it['stc'];
			struct['result']['objs'].append(it);
			strs += it['str'] + ',';
		if len(strs) >= 2:
			strs = strs[0:-1];
		ComFuncs._set_msg(struct,self.data['msg']['throw'],strs);

	def _get_unknow_info(self,struct,super_b):
		struct['result']['action'] = 'unknow';
		ComFuncs._set_msg(struct,self.data['msg']['unknow']);
