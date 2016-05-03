#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
import scene_param as SceneParam
from common import logging
from myexception import MyException
from scene_base import SceneBase
import scene_param as SceneParam

#添加多个闹钟场景 或者带有时间
class SceneMadd(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene add more clock......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				ck_num = SceneParam._get_num_cks(struct);
				if ck_num == 1 or ck_num == 0:
					struct['result']['msg'] = self.data['msg']['un_see'][0];
					struct['step'] = 'end';
					return None;
				struct['ck_num'] = ck_num;
				if struct['ttag'].find('time') == -1:
					struct['result']['msg'] = (self.data['msg']['set_mtime'][0] %(ck_num));
					struct['step'] = 'set_time';
					return None;
			self._add_more_cks(struct['ck_num'],struct,super_b);
			del struct['ck_num'];
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _set_time(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			myclock['time'] = struct['ck_time']['time'];
			del struct['ck_time'];
		else:
			struct['result']['msg'] = self.data['msg']['unknow_time'];
			struct['step'] = 'end';
		return 0;

	def _set_able(self,struct,super_b):
		myclock = super_b.myclock
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
		else:
			myclock['able'] = dict();
			myclock['able']['type'] = 'week';
			myclock['able']['able'] = '127'

	def _add_more_cks(self,num,struct,super_b):
		onum = num;
		while True:
			if num <= 0: break;
			super_b.myclock = dict();
			if len(struct['Times']) <> num:
				struct['result']['msg'] = self.data['msg']['less_time'][0];
				return None;
			SceneParam._find_time(struct);
			SceneParam._calc_able(struct);
			self._set_time(struct,super_b);
			self._set_able(struct,super_b);
			num = num - 1;
			super_b.myclock['key'] = super_b.myclock['time'];
			super_b.clocks[super_b.myclock['time']] = super_b.myclock;
			del struct['Times'][0];
		if struct.has_key('Times'): del struct['Times'];
		struct['result']['msg'] = (self.data['msg']['madd_succ'][0] %(onum));

