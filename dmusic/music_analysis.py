#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from music_base import MusicBase
import com_funcs as ComFuncs

#处理 音乐 场景
class MusicAnalysis(MusicBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into music analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';
			self._fetch_all_types(struct);

			if struct['step'] == 'start':
				func = self._fetch_func(struct);
				if func == 'get':
					self._get_music(struct,super_b);
				elif func == 'next':
					self._get_next_music(struct,super_b);
				elif func == 'repeat':
					self._get_repeat_music(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_all_types(self,struct):
		self._fetch_type(struct,'LocalPrep');
		self._fetch_type(struct,'PerPronom');
		self._fetch_type(struct,'PrepCom');
		self._fetch_type(struct,'VerbCom');

	def _fetch_type(self,struct,key):
		if struct.has_key(key):
			for item in struct[key]: struct[item['str']] = item;
			del struct[key];

	def _fetch_func(self,struct):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			reg = reg + struct[istr]['stype'];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

	#获取指定所属的音乐
	def _get_music(self,struct,super_b):
		owner = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item.has_key('type') and item['type'] == 'STH':
				if item.has_key('BELONGS'):
					belong = item['BELONGS'];
					owner = belong['stype'];
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
