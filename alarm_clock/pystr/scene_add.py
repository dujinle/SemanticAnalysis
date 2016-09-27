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
import common,pgsql
from common import logging
from myexception import MyException
from base import Base
import scene_param as SceneParam

#添加闹钟场景 或者带有时间
class SceneAdd(Base):

	def encode(self,struct,super_b):
		try:
			print 'go into scene add action......';
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				msg_id = SceneParam._get_random_id(len(self.data['msg']['start_msg']));
				struct['result']['msg'] = self.data['msg']['start_msg'][msg_id];
				super_b.myclock = dict();
				self._send_msg(struct['result'])
				#开始询问时间设置
				if struct['ttag'].find('time') == -1:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['set_time']));
					struct['result']['msg'] = self.data['msg']['set_time'][msg_id];
					struct['step'] = 'set_time';
					return None;
				else:
					SceneParam._find_time(struct);
					SceneParam._calc_able(struct);
					self._set_time(struct,super_b);
					self._set_able(struct,super_b);
			elif struct['step'] == 'set_time':
				SceneParam._find_time(struct);
				SceneParam._calc_able(struct);
				if self._set_time(struct,super_b) == -1: return None;
				self._set_able(struct,super_b);
			struct['step'] = 'trans';
		except Exception as e:
			raise MyException(format(e));

	def _set_time(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			times = struct['ck_time']['time'];
			hour = int(times.split(':')[0]);
			if hour >= self.data['common']['getup_time'][0] \
				and hour <= self.data['common']['getup_time'][1]:
				struct['ck_scene'] = 'ck_getup_add';
				myclock['type'] = 'getup';
				#时间设置完成回应信息
				msg_id = SceneParam._get_random_id(len(self.data['msg']['add_getup_ck']));
				struct['result']['msg'] = self.data['msg']['add_getup_ck'][msg_id];
				#todo send msg......
				self._send_msg(struct['result'])
			else:
				struct['ck_scene'] = 'ck_agenda_add';
				myclock['type'] = 'agenda';
				#时间设置完成回应信息
				msg_id = SceneParam._get_random_id(len(self.data['msg']['add_agenda_ck']));
				struct['result']['msg'] = self.data['msg']['add_agenda_ck'][msg_id];
				#todo send msg......
				self._send_msg(struct['result'])
			myclock['time'] = struct['ck_time']['time'];
			del struct['ck_time'];
		else:
			msg_id = SceneParam._get_random_id(len(self.data['msg']['unknow_time']));
			struct['result']['msg'] = self.data['msg']['unknow_time'][msg_id];
			struct['step'] = 'end';
			return -1;
		return 0;

	def _set_able(self,struct,super_b):
		myclock = super_b.myclock
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
