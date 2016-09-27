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
import common,alarm_common,pgsql,scene_param
from common import logging
from myexception import MyException
from base import Base
import scene_param as SceneParam

#添加多个闹钟场景 或者带有时间
class SceneMadd(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene add more clock......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				ck_num = SceneParam._get_cks_num(struct);
				if ck_num == 1 or ck_num == 0:
					struct['result']['msg'] = self.data['msg']['un_see'][0];
					struct['step'] = 'end';
					return None;
				if struct['ttag'].find('time') <> -1:
					self._add_more_cks(ck_num,struct,super_b);
					struct['step'] = 'end';
				else:
					struct['result']['msg'] = (self.data['msg']['set_mtime'][0] %(ck_num));
					struct['step'] = 'set_time';
					struct['ck_num'] = ck_num;
					return None;
			elif struct['step'] == 'set_time':
				self._add_more_cks(struct['ck_num'],struct,super_b);
				del struct['ck_num'];
			struct['step'] = 'end';
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
				struct['result']['msg'] = self.data['msg']['add_getup_ck'];
				#todo send msg......
				self._send_msg(struct['result'])
			else:
				struct['ck_scene'] = 'ck_agenda_add';
				myclock['type'] = 'agenda';
				#时间设置完成回应信息
				struct['result']['msg'] = self.data['msg']['add_agenda_ck'];
				#todo send msg......
				self._send_msg(struct['result'])
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

	def _add_more_cks(self,num,struct,super_b):
		idx = 0;
		while True:
			if idx >= num: break;
			super_b.myclock = dict();
			if len(struct['intervals']) <> num:
				struct['result']['msg'] = self.data['msg']['less_time'][0];
				break;
			SceneParam._find_time(struct);
			self._set_time(struct,super_b);
			idx = idx + 1;
			super_b.clocks[super_b.myclock['time']] = super_b.myclock;
			del struct['intervals'][0];
		if struct.has_key('intervals'): del struct['intervals'];
		struct['result']['msg'] = (self.data['msg']['madd_succ'][0] %(num));

