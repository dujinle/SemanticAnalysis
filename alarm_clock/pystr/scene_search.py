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
import common
from myexception import MyException
from common import logging
import scene_param as SceneParam

from scene_base import SceneBase
class SceneSearch(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into search scene......');
			if not struct.has_key('step'): struct['step'] = 'start';
			if struct['step'] == 'start':
				struct['result']['msg'] = self.data['msg']['set_start'];
				#self.send_msg(struct);
				#开始参数设置向导
				cks = self._find_cks(struct,super_b);
				self._post_clocks(cks,struct,super_b);
				struct['step'] = 'end';
		except Exception as e:
			raise MyException(format(e));

	def _find_cks(self,struct,super_b):
		cks = list();
		if struct['ttag'].find('_see_has_some_clock') <> -1:
			cks = super_b.clocks.keys();
			return cks;
		elif len(re.findall('_time_has_some.*_thing',struct['ttag'])) > 0:
			cks = SceneParam._find_cks_bytime(struct,super_b);
			return cks;
		elif len(re.findall('_time_has_what.*_thing',struct['ttag'])) > 0:
			cks = SceneParam._find_cks_bytime(struct,super_b);
			return cks;
		elif len(re.findall('_time.*_yes_what_info',struct['ttag'])) > 0:
			cks = SceneParam._find_cks_bytime(struct,super_b);
			return cks;
		elif len(re.findall('_remind_yes((_what_shihou)|(_wtime))',struct['ttag'])) > 0:
			cks = SceneParam._find_cks_byinfo(struct,super_b);
			return cks;
		elif len(re.findall('_clock_yes((_what_shihou)|(_wtime))',struct['ttag'])) > 0:
			cks = SceneParam._find_cks_byinfo(struct,super_b);
			return cks;
		elif len(re.findall('_time_clock_yes_what',struct['ttag'])) > 0:
			cks = SceneParam._find_cks_bytime(struct,super_b);
			return cks;
		elif struct['ttag'].find('_after_has_what_thing') <> -1:
			cks = SceneParam._find_cks_after(struct,super_b);
			return cks;
		elif struct['ttag'].find('_workoff_after_has_some') <> -1:
			cks = SceneParam._find_cks_tagtime('workoff',super_b);
			return cks;
		elif struct['ttag'].find('_prep_info_yes_what') <> -1:
			inum = SceneParam._get_cks_num(struct);
			keys = super_b.clocks.keys();
			cks.append(keys[inum - 1]);
			return cks;
		elif len(re.findall('see.*_prep_clock',struct['ttag'])) > 0:
			inum = SceneParam._get_cks_num(struct);
			keys = super_b.clocks.keys();
			cks.append(keys[inum - 1]);
			return cks;
		return cks;

	def _post_clocks(self,cks,struct,super_b):
		struct['result']['clocks'] = list();
		first_ck = None;
		for ck in cks:
			clock = super_b.clocks[ck];
			if first_ck is None: first_ck = clock;
			struct['result']['clocks'].append(clock);
		if len(cks) > 0:
			msg_id = SceneParam._get_random_id(len(self.data['msg']['ck_num']));
			struct['result']['msg'] = (self.data['msg']['ck_num'][msg_id] %len(cks));
		else:
			msg_id = SceneParam._get_random_id(len(self.data['msg']['ck_unknow']));
			struct['result']['msg'] = self.data['msg']['ck_unknow'][msg_id]
