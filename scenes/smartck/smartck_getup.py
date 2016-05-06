#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys,common
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as SceneParam
import smartck_common as SmartckCom

class SmartckGetup(SceneBase):

	def encode(self,struct,super_b):
		try:
			if not struct.has_key('ck_scene'): return None;
			if struct['ck_scene'] <> 'ck_getup_add': return None;
			if not struct.has_key('step'): struct['step'] = 'start';
			SmartckCom._fetch_time(struct);
			SmartckCom._calc_able(struct);
			logging.info('go into scene get up......');
			if struct['step'] == 'start':
				super_b.myclock = dict();
				self._set_getup_info(struct,super_b);
				return None;
			if struct['step'] == 'trans':
				self._set_clock_info(struct,super_b);
			elif struct['step'] == 'set_time':
				self._set_getup_info(struct,super_b);
				return None;
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_reply(self,struct,super_b):
		ck = super_b.myclock;
		usual_time = self.data['getup'];
		mytime = ck['time'];
		if usual_time['type'] == 'time':
			uhour = usual_time['value'].split(':')[0];
			umin = usual_time['value'].split(':')[1];
			mhour = mytime.split(':')[0];
			mmin = mytime.split(':')[1];
			if int(uhour) > int(mhour) and int(mhour) > 3:
				SceneParam._set_msg(struct,self.data['msg']['rise_early']);
			elif (int(uhour) <= int(mhour) or (int(uhour) == int(mhour) and int(mmin) >= int(umin)))\
				and int(mhour) <= 8:
					SceneParam._set_msg(struct,self.data['msg']['rise_common']);
			elif int(mhour) > 8 and int(mhour) <= 11:
				SceneParam._set_msg(struct,self.data['msg']['rise_late']);
			else:
				SceneParam._set_msg(struct,self.data['msg']['rise_common']);

	def _set_clock_info(self,struct,super_b):
		if super_b.myclock.has_key('name'):
			super_b.myclock['key'] = super_b.myclock['name'];
			super_b.clocks[super_b.myclock['key']] = super_b.myclock;
		elif super_b.myclock.has_key('info'):
			super_b.clocks[super_b.myclock['info']] = super_b.myclock;
			super_b.myclock['key'] = super_b.myclock['info'];
		else:
			super_b.clocks[super_b.myclock['time']] = super_b.myclock;
			super_b.myclock['key'] = super_b.myclock['time'];
		self._fetch_reply(struct,super_b);

	def _set_getup_info(self,struct,super_b):
		self._set_time(struct,super_b);
		self._set_name(struct,super_b);
		self._set_able(struct,super_b);
		self._check_param(struct,super_b);

	def _set_time(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_time'):
			times = struct['ck_time']['time'];
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
			myclock['able']['able'] = '127';

	def _set_name(self,struct,super_b):
		myclock = super_b.myclock;
		if struct.has_key('ck_name'):
			myclock['name'] = struct['ck_name'];
			del struct['ck_name'];
		else:
			myclock['name'] = u'起床';

	def _check_param(self,struct,super_b):
		if not super_b.has_key('ck_time'):
			SceneParam._set_msg(struct,self.data['msg']['set_time']);
			struct['step'] = 'set_time';
		else:
			self._set_clock_info(struct,super_b);
			struct['step'] = 'end';

