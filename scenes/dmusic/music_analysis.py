#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

#处理 音乐 场景
class MusicAnalysis(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into music analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			if struct['step'] == 'start':
				func = self._fetch_func(struct);
				print 'music func ',func,'......'
				if func == 'get':
					self._get_music(struct,super_b);
				elif func == 'next':
					self._get_next_music(struct,super_b);
				elif func == 'repeat':
					self._get_repeat_music(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	#获取指定所属的音乐
	def _get_music(self,struct,super_b):
		owner = None;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];

			if item.has_key('type'):
				if item['type'] == 'RP' or item['type'] == 'NB':
					owner = item['str'];
					break;
		if owner is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			musics = super_b.get_favorite(owner);
			if musics is None:
				ComFuncs._set_msg(struct,self.data['msg']['unknow']);
				return None;
			struct['result']['msg'] = ' '.join(musics);

	def _get_next_music(self,struct,super_b):
		tdic = dict();
		tdic['scene'] = 'MUSIC';
		tdic['status'] = 'NEXT';
		struct['result']['att'] = tdic;
		ComFuncs._set_msg(struct,self.data['msg']['next_succ']);

	def _get_repeat_music(self,struct,super_b):
		tdic = dict();
		tdic['scene'] = 'MUSIC';
		tdic['status'] = 'REPEAT';
		struct['result']['att'] = tdic;
		ComFuncs._set_msg(struct,self.data['msg']['repeat_succ']);
