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
import common,datetime,math
from common import logging
from myexception import MyException
from scene_base import SceneBase
import scene_param as SceneParam

#删除指定的闹钟场景设置
class SceneDel(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene delete action......');
			if not struct.has_key('step'): struct['step'] = 'start';
			#启动时响应回复
			if struct['step'] == 'start':
				cks = self._find_cks(struct,super_b);
				if len(cks) > 0:
					self._del_cks(cks,super_b,struct);
				else:
					SceneParam._set_msg(struct,self.data['msg']['ck_unknow']);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _del_cks(self,cks,super_b,struct):
		info = '';
		if struct['ttag'].find('_only_left_time') <> -1:
			for ck in super_b.clocks.keys():
				if ck in cks: continue;
				clk = super_b.clocks[ck];
				if clk.has_key('info'): info = clk['info'];
				del super_b.clocks[ck];
		else:
			for ck in cks:
				if super_b.clocks.has_key(ck):
					clk = super_b.clocks[ck];
					if clk.has_key('info'): info = clk['info'];
					del super_b.clocks[ck];
		if len(cks) > 1:
			struct['result']['msg'] = (self.data['msg']['del_cks'][0] %(info,u'等'));
		else:
			struct['result']['msg'] = (self.data['msg']['del_cks'][0] %(info,''));

	def _find_cks(self,struct,super_b):
		cks = list();
		did = 2;
		hid = 3;
		mid = 4;
		if struct.has_key('intervals'):
			inters = struct['intervals'];
			if struct['ttag'].find('_time_clock') <> -1\
				or struct['ttag'].find('_time_all_clock') <> -1\
				or struct['ttag'].find('_only_left_time') <> -1:
				if inters[0]['scope'] == 'hour':
				#找到某段时间的闹钟 晚上所有的闹钟
					start = inters[0]['start'];
					end = inters[0]['end'];
					for ck in super_b.clocks:
						clock = super_b.clocks[ck];
						hour = int(clock['time'].split(':')[0]);
						mins = int(clock['time'].split(':')[1]);
						if hour > start[hid] or (hour == start[hid] and start[mid] <= mins):
							if hour < end[hid] or (hour == end[hid] and end[mid] >= mins):
								cks.append(ck);
					del struct['intervals'];
					return cks;
				elif inters[0]['scope'] == 'day':
				#找到某天的闹钟 今天的闹钟
					start = inters[0]['start'];
					end = inters[0]['end'];
					dat = datetime.date(int(start[0]),int(start[1]),int(start[2]));
					week = dat.weekday();
					able = math.pow(2,week);
					if end[did] - start[did] > 1: able = able + math.pow(2,week + 1);
					for ck in super_b.clocks:
						clock = super_b.clocks[ck];
						if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
							cks.append(ck);
					del struct['intervals'];
					return cks;
		else:
			if struct['ttag'].find('_nouse_del') <> -1:
				for ck in super_b.clocks:
					clk = super_b.clocks[ck]
					if clk['status']['type'] == 'close':
						cks.append(ck);
			elif struct['ttag'].find('_pastdue_clock') <> -1:
				for ck in super_b.clocks:
					clk = super_b.clocks[ck];
					if clk.has_key('due') and ck['due']['type'] == 'past':
						cks.append(ck);
					elif not clk.has_key('due'):
						cks.append(ck);
			elif struct['ttag'].find('_prep') <> -1:
				for tnum in SceneParam.num.keys():
					if tnum in struct['inlist']:
						ckeys = super_b.clocks.keys();
						cks.append(ckeys[SceneParam.num[tnum]]);
			elif struct['ttag'].find('_just_that') <> -1:
				if not super_b.prev_ck is None:
					cks.append(super_b.prev_ck);
		return cks
