#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,math
from common import logging
from myexception import MyException
from scene_base import SceneBase
import scene_param as SceneParam

#新增日程闹钟 或者带有时间的
class SceneAgenda(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene agenda');
			if not struct.has_key('step'): struct['step'] = 'start';
			if struct['step'] == 'start' and SceneParam._if_exist(struct,super_b):
				msg_id = SceneParam._get_random_id(len(self.data['msg']['ck_exist']));
				struct['result']['msg'] = self.data['msg']['ck_exist'][msg_id]
				struct['step'] = 'end';
				logging.info('the alarm clock is exist so add failed!')
				return None;
			elif struct['step'] == 'start':
				super_b.myclock = dict();
				self._set_agenda_info(struct,super_b);
				if struct['ttag'].find('time') == -1:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['set_time']));
					struct['result']['msg'] = self.data['msg']['set_time'][msg_id];
					struct['step'] = 'set_time';
					return None;
				else:
					SceneParam._find_time(struct);
					SceneParam._calc_able(struct);
					self._set_clock(struct,super_b);
			elif struct['step'] == 'trans':
				self._set_agenda_info(struct,super_b);
			elif struct['step'] == 'set_time':
				SceneParam._find_time(struct);
				SceneParam._calc_able(struct);
				self._set_clock(struct,super_b);
			if super_b.myclock.has_key('info'):
				super_b.clocks[super_b.myclock['info']] = super_b.myclock;
				super_b.myclock['key'] = super_b.myclock['info'];
				msg_id = SceneParam._get_random_id(len(self.data['msg']['set_succ']));
				struct['result']['msg'] = (self.data['msg']['set_succ'][msg_id] %(super_b.myclock['info']));
			else:
				super_b.clocks[super_b.myclock['time']] = super_b.myclock;
				super_b.myclock['key'] = super_b.myclock['time'];
				msg_id = SceneParam._get_random_id(len(self.data['msg']['set_succ']));
				struct['result']['msg'] = (self.data['msg']['set_succ'][msg_id] %(''));
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _set_clock(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			times = struct['ck_time']['time'];
			myclock['type'] = 'agenda';
			myclock['time'] = times;
			del struct['ck_time'];
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
		elif not struct.has_key('ck_able'):
			week = SceneParam._get_cur_week();
			myclock['able'] = dict();
			myclock['able']['type'] = 'week';
			myclock['able']['able'] = math.pow(2,week);
		if struct.has_key('intervals'): del struct['intervals'];
		return 0;

	def _set_agenda_info(self,struct,super_b):
		myclock = super_b.myclock;
		if struct['text'].find(self.data['drink']) <> -1:
			tid = struct['text'].find(self.data['drink']);
			myclock['info'] = struct['text'][tid:];
		elif struct['ttag'].find('_cout') <> -1:
			myclock['info'] = self.data['cout'];
		elif struct['ttag'].find('_go') <> -1:
			tid = struct['inlist'].index(u'去');
			myclock['info'] = struct['inlist'][tid + 1];
		elif struct['ttag'].find('_remind_me') <> -1:
			tid = struct['text'].find(u'提醒我') + 3;
			myclock['info'] = struct['text'][tid:];
		elif struct['ttag'].find('_meeting') <> -1:
			myclock['info'] = self.data['meeting'];
		elif struct['ttag'].find('_info') <> -1:
			for content in self.data['infois']:
				if struct['text'].find(content) <> -1:
					tid = struct['text'].find(content) + len(content);
					myclock['info'] = struct['text'][tid:];
					break;
		if myclock.has_key('info') and myclock['info'] == '':
			del myclock['info'];
