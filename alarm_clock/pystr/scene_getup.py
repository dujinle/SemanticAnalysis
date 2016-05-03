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
			print 'go into scene get up......';
			if not struct.has_key('step'): struct['step'] = 'start';
			if struct['step'] == 'start' and SceneParam._if_exist(struct,super_b):
				msg_id = SceneParam._get_random_id(len(self.data['msg']['ck_exist']));
				struct['result']['msg'] = self.data['msg']['ck_exist'][msg_id]
				struct['step'] = 'end';
				logging.info('the alarm clock is exist so add failed!')
				return None;
			elif struct['step'] == 'start':
				super_b.myclock = dict();
				if struct['ttag'].find('time') == -1:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['set_time']));
					struct['result']['msg'] = self.data['msg']['set_time'][0];
					struct['step'] = 'set_time';
					return None;
			if struct['step'] <> 'trans':
				SceneParam._find_time(struct);
				SceneParam._calc_able(struct);
				if self._set_clock(struct,super_b) == -1:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['unknow_time']));
					struct['result']['msg'] = self.data['msg']['unknow_time'][msg_id];
					struct['step'] = 'end';
					return None;
			self._analysis_mytag(struct,super_b);
			if super_b.myclock.has_key('name'):
				super_b.myclock['key'] = super_b.myclock['name'];
			else:
				super_b.myclock['key'] = super_b.myclock['time'];
			super_b.clocks[super_b.myclock['key']] = super_b.myclock;
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _analysis_mytag(self,struct,super_b):
		ck = super_b.myclock;
		if struct.has_key('tag') and struct['tag'].has_key(u'起床'):
			if not ck.has_key('time'): return False;
			usual_time = struct['tag'][u'起床'];
			mytime = ck['time'];
			if usual_time['type'] == 'time':
				uhour = usual_time['value'].split(':')[0];
				umin = usual_time['value'].split(':')[1];
				mhour = mytime.split(':')[0];
				mmin = mytime.split(':')[1];
				if int(uhour) > int(mhour) and int(mhour) > 3:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['rise_early']));
					struct['result']['msg'] = self.data['msg']['rise_early'][msg_id];
				elif (int(uhour) <= int(mhour) or (int(uhour) == int(mhour) and int(mmin) >= int(umin)))\
					and int(mhour) <= 8:
						msg_id = SceneParam._get_random_id(len(self.data['msg']['rise_common']));
						struct['result']['msg'] = self.data['msg']['rise_common'][msg_id];
				elif int(mhour) > 8 and int(mhour) <= 11:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['rise_late']));
					struct['result']['msg'] = self.data['msg']['rise_late'][msg_id];
				else:
					msg_id = SceneParam._get_random_id(len(self.data['msg']['rise_common']));
					struct['result']['msg'] = self.data['msg']['rise_common'][msg_id];
				return True;
		return False;

	def _set_clock(self,struct,super_b):
		myclock = super_b.myclock;
		myclock['type'] = 'getup';
		if not struct.has_key('ck_time'): return -1;
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
		if struct.has_key('ck_name'):
			myclock['name'] = struct['ck_name'];
			del struct['ck_name'];
		if struct.has_key('intervals'): del struct['intervals'];
		return 0;
