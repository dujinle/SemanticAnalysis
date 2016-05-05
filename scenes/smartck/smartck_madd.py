#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
import re,time
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as SceneParam
import smartck_common as SmartckCom

#添加多个闹钟场景 或者带有时间
class SmartckMadd(SceneBase):

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_madd': return None;
			logging.info('go into scene add more clock......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				ck_num = self._get_ck_num(struct);
				if ck_num == 1 or ck_num == 0:
					SceneParam._set_msg(struct,self.data['msg']['un_see']);
					struct['step'] = 'end';
					return None;
				struct['ck_num'] = ck_num;
				if struct['ttag'].find('TIME') == -1:
					SceneParam._set_msg(struct,self.data['msg']['set_mtime']);
					struct['step'] = 'set_time';
					return None;
			self._add_more_cks(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _set_time(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			myclock['time'] = struct['ck_time']['time'];
			del struct['ck_time'];

	def _set_able(self,struct,super_b):
		myclock = super_b.myclock
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
		else:
			myclock['able'] = dict();
			myclock['able']['type'] = 'week';
			myclock['able']['able'] = '127'

	def _get_ck_num(self,struct):
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item['type'] == 'NUM':
				num = int(item['str']);
				return num;
		return 0;

	def _add_more_cks(self,struct,super_b):

		onum = struct['ck_num'];
		while True:
			if onum <= 0: break;
			super_b.myclock = dict();
			SceneParam._fetch_time(struct);
			SceneParam._calc_able(struct);
			if not struct.has_key('ck_time'):
				SceneParam._set_msg(struct,self.data['msg']['set_mtime']);
				struct['step'] = 'set_time';
				struct['ck_num'] = onum;
				return None;
			self._set_time(struct,super_b);
			self._set_able(struct,super_b);
			num = num - 1;
			super_b.myclock['key'] = super_b.myclock['time'];
			super_b.clocks[super_b.myclock['time']] = super_b.myclock;
		SceneParam._set_msg(struct,self.data['msg']['madd_succ']);
