#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math
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
from scene_base import SceneBase
import scene_param as SceneParam

class SceneGetup(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into scene get up');
			if not struct.has_key('step'): struct['step'] = 'start';
			if struct['step'] == 'start' and SceneParam._if_exist(struct,super_b):
				msg_id = SceneParam._get_random_id(len(self.data['msg']['ck_exist']));
				struct['result']['msg'] = self.data['msg']['ck_exist'][msg_id]
				struct['step'] = 'end';
				logging.info('the alarm clock is exist so add failed!')
				return None;
			elif struct['step'] == 'start':
				if super_b.myclock is None: super_b.myclock = dict();
				if struct['ttag'].find('time') == -1:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['set_time']));
					struct['result']['msg'] = self.data['msg']['set_time'][0];
					struct['step'] = 'set_time';
					return None;
				else:
					SceneParam._find_time(struct);
					SceneParam._calc_able(struct);
			elif struct['step'] == 'set_time':
				SceneParam._find_time(struct);
				SceneParam._calc_able(struct);
			self._set_clock(struct,super_b);
			self._analysis_mytag(struct,super_b);
			super_b.myclock['key'] = super_b.myclock['time'];
			super_b.clocks[super_b.myclock['time']] = super_b.myclock;
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _analysis_mytag(self,struct,super_b):
		ck = super_b.myclock;
		print 'go into _analysis_mytag......'
		if struct.has_key('tag') and struct['tag'].has_key(u'起床'):
			if not ck.has_key('time'): return False;
			usual_time = struct['tag'][u'起床'];
			mytime = ck['time'];
			if usual_time['type'] == 'time':
				uhour = usual_time['value'].split(':')[0];
				umin = usual_time['value'].split(':')[1];
				mhour = mytime.split(':')[0];
				mmin = mytime.split(':')[1];
				if int(uhour) > int(mhour):
					msg_id = SceneParam._get_random_id(len(self.data['msg']['rise_early']));
					struct['result']['msg'] = self.data['msg']['rise_early'][msg_id];
				elif int(uhour) == int(mhour) and int(mmin) < int(umin) + 20:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['rise_early']));
					struct['result']['msg'] = self.data['msg']['rise_early'][msg_id];
				else:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['rise_late']));
					struct['result']['msg'] = self.data['msg']['rise_late'][msg_id];
				return True;
		return False;

	def _set_clock(self,struct,super_b):
		myclock = super_b.myclock;
		myclock['type'] = 'getup';
		if struct.has_key('ck_time'):
			times = struct['ck_time']['time'];
			myclock['time'] = times;
			del struct['ck_time'];
		if struct.has_key('ck_able'):
			myclock['able'] = struct['ck_able'];
			del struct['ck_able'];
		else:
			myclock['able'] = dict();
			myclock['able']['type'] = 'week';
			myclock['able']['able'] = math.pow(2,7) - 1;
		if struct.has_key('intervals'): del struct['intervals'];
		return 0;
