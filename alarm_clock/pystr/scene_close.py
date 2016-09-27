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
from common import logging
from myexception import MyException
import scene_param as SceneParam
from base import Base

class SceneClose(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene close action......');
			if not struct.has_key('step'): struct['step'] = 'start';

			#启动时响应回复
			if struct['step'] == 'start':
				cks = self._which_ck_close(struct,super_b);
				struct['result']['msg'] = (self.data['msg']['close_start'][0] %len(cks))
				#todo send msg......
				if len(cks) > 0:
					close_num = self._close_cks(cks,super_b);
					msg_id = SceneParam._get_random_id(len(self.data['msg']['close_succ']));
					struct['result']['msg'] = (self.data['msg']['close_succ'][msg_id] %close_num);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _which_ck_close(self,struct,super_b):
		cks = list();
		if struct['ttag'].find('_time_to_time') <> -1:
			start = struct['intervals'][0]['start'];
			end = struct['intervals'][1]['start'];
			hid = 3;
			mid = 4;
			for ck in super_b.clocks:
				clock = super_b.clocks[ck];
				hour = int(clock['time'].split(':')[0]);
				mins = int(clock['time'].split(':')[1]);
				if hour > start[hid] or (hour == start[hid] and start[mid] <= mins):
					if hour < end[hid] or (hour == end[hid] and end[mid] >= mins):
						cks.append(ck);
		elif struct['ttag'].find('_time') <> -1:
			start = struct['intervals'][0]['start'];
			end = struct['intervals'][0]['end'];
			hid = 3;
			mid = 4;
			for ck in super_b.clocks:
				clock = super_b.clocks[ck];
				hour = int(clock['time'].split(':')[0]);
				mins = int(clock['time'].split(':')[1]);
				if start[0] == 'null':
					if hour < end[hid] or (hour == end[hid] and mins <= end[mid]):
						cks.append(ck);
				elif end[0] == 'null':
					if hour < start[hid] or (hour == start[hid] and mins <= start[mid]):
						cks.append(ck);
				else:
					if hour == start[hid] and mins == start[mid]:
						cks.append(ck);
		elif struct['ttag'].find('_close_clock') <> -1:
			cks = super_b.clocks.keys();
		return cks;

	def _close_cks(self,cks,super_b):
		close_num = 0;
		for ck in cks:
			clock = super_b.clocks[ck];
			if not clock.has_key('status'):
				clock['status'] = dict();
				clock['status']['type'] = 'close';
				close_num = close_num + 1;
			elif clock['status']['type'] <> 'close':
				clock['status']['type'] = 'close';
				close_num = close_num + 1;
		return close_num;
