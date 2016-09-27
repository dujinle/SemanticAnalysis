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
import common,alarm_common
from myexception import MyException
from common import logging

from base import Base

#直接设置闹铃生效日期
class SceneAble(Base):

	def encode(self,struct,super_b):
		try:
			logging.info('go into set alarm date able......');
			if super_b.myclock is None:
				struct['result']['msg'] = self.data['msg']['ck_unknow'][0];
				struct['code'] = 'exit';
				return None;
			if not sturct.has_key('step'): sturct['step'] = 'start';

			if struct['step'] == 'start':
				self._encode_date_able(struct,super_b);
				self._set_able(struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _encode_date_able(self,struct,super_b):
		myclock = super_b.myclock;
		tdic = dict();
		if myclock.has_key('able'): tdic = myclock['able'];

		tag = '';
		for ck in struct['clocks']:
			tag = tag + ck['type'];
		if tag.find('_workday') <> -1:
			tdic['type'] = 'workday'
			tdic['able'] = math.pow(2,5) - 1;
		elif tag.find('_workend') <> -1:
			tdic['type'] = 'workend';
			tdic['able'] = math.pow(2,7) - math.pow(2,5);
		elif tag.find('_time_no_call') <> -1:
			able = 127;
			if tdic.has_key('able'): able = tdic['able'];
			for inter in struct['intervals']:
				if myinterval['scope'] == 'day':
					times = inter['start'];
					dat = datetime.date(int(times[0]),int(times[1]),int(times[2]));
					week = dat.weekday();
					able = able - math.pow(2,week);
			tdic['able'] = able;
			tdic['type'] = 'day';
		elif tag.find('_time_call') <> -1:
			able = 0;
			if tdic.has_key('able'): able = tdic['able'];
			for inter in struct['intervals']:
				if myinterval['scope'] == 'day':
					times = inter['start'];
					dat = datetime.date(int(times[0]),int(times[1]),int(times[2]));
					week = dat.weekday();
					able = able + math.pow(2,week);
			tdic['able'] = able;
			tdic['type'] = 'day';
		if tdic.has_key('type'): struct['ck_able'] = tdic;

	def _set_able(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
			struct['result']['msg'] = self.data['msg']['set_able_succ'][0];
		else:
			struct['result']['msg'] = self.data['msg']['able_nothing'][0];
