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
import pgsql,collections
import common
from common import logging
from myexception import MyException

from scene_add import SceneAdd
from scene_getup import SceneGetup
from scene_agenda import SceneAgenda
from scene_search import SceneSearch
from scene_delay import SceneDelay
from scene_stop import SceneStop
from scene_open import SceneOpen
from scene_close import SceneClose
from scene_prompt import ScenePrompt
from scene_able import SceneAble
from scene_del import SceneDel
from scene_madd import SceneMadd
from scene_time import SceneTime
from scene_bell import SceneBell
from scene_sbell import SceneSBell

from concept import Concept
from dist_scene import DistScene
from prev_scene import PrevScene
import scene_param as SceneParam

msg = [
	u'我还在实习期，还需要多点时间熟悉情况',
	u'难死宝宝了，让我再学习学习吧',
	u'这事儿现在搞不定，您再等等呗'
];
err_msg = ["好头疼，我得再学习学习..."];
class SEngin():

	def __init__(self,wordseg):
		self.clocks = collections.OrderedDict();
		self.myclock = None;

		self.scene_con = Concept();
		self.dist_scene = DistScene();
		self.prev_scene = PrevScene();
		self.wordseg = wordseg;

		self.scene_add = SceneAdd();
		self.scene_getup = SceneGetup();
		self.scene_agenda = SceneAgenda();
		self.scene_search = SceneSearch();
		self.scene_delay = SceneDelay();
		self.scene_stop = SceneStop();
		self.scene_open = SceneOpen();
		self.scene_close = SceneClose();
		self.scene_prompt = ScenePrompt();
		self.scene_able = SceneAble();
		self.scene_del = SceneDel();
		self.scene_madd = SceneMadd();
		self.scene_time = SceneTime();
		self.scene_bell = SceneBell();
		self.scene_sbell = SceneSBell();

	def init(self,fdir):
		self.scene_con.load_data(fdir + '/concept.txt');
		self.dist_scene.load_data(fdir + '/dist_scene.txt');

		self.scene_add.load_data(fdir + '/scene_add.txt');
		self.scene_getup.load_data(fdir + '/scene_getup.txt');
		self.scene_agenda.load_data(fdir + '/scene_agenda.txt');
		self.scene_search.load_data(fdir + '/scene_search.txt');
		self.scene_delay.load_data(fdir + '/scene_delay.txt');
		self.scene_stop.load_data(fdir + '/scene_stop.txt');
		self.scene_open.load_data(fdir + '/scene_open.txt');
		self.scene_close.load_data(fdir + '/scene_close.txt');
		self.scene_prompt.load_data(fdir + '/scene_prompt.txt');
		self.scene_able.load_data(fdir + '/scene_able.txt');
		self.scene_del.load_data(fdir + '/scene_del.txt');
		self.scene_madd.load_data(fdir + '/scene_madd.txt');
		self.scene_time.load_data(fdir + '/scene_time.txt');
		self.scene_bell.load_data(fdir + '/scene_bell.txt');
		self.scene_sbell.load_data(fdir + '/scene_sbell.txt');


	def _init(self,struct):
		if struct.has_key('clocks'): del struct['clocks'];
		if struct.has_key('ck_name'): del struct['ck_name'];
		if struct.has_key('ck_time'): del struct['ck_time'];
		if struct.has_key('result'): struct['result'] = dict();
		if struct.has_key('ttag'): del struct['ttag'];

	def _tail(self,struct):
	#	if struct.has_key('clocks'): del struct['clocks'];
	#	if struct.has_key('ck_name'): del struct['ck_name'];
		if struct.has_key('ck_time'): del struct['ck_time'];
		if struct.has_key('ttag'): del struct['ttag'];
	#	if struct.has_key('inlist'): del struct['inlist'];
		if struct.has_key('tag'): del struct['tag'];
		if struct.has_key('mood'): del struct['mood'];


	def encode(self,struct):
		try:
			self._init(struct);
			self.prev_scene.encode(struct);
			struct['inlist'] = self.wordseg.tokens(struct['text']);

			self.scene_con.encode(struct);
			self.dist_scene.encode(struct);
			if struct.has_key('ck_scene'):
				if struct['ck_scene'] == 'ck_add':
					self.scene_add.encode(struct,self);
				if struct['ck_scene'] == 'ck_getup_add':
					self.scene_getup.encode(struct,self);
				if struct['ck_scene'] == 'ck_agenda_add':
					self.scene_agenda.encode(struct,self);
				if struct['ck_scene'] == 'ck_search':
					self.scene_search.encode(struct,self);
				if struct['ck_scene'] == 'ck_delay':
					self.scene_delay.encode(struct,self);
				if struct['ck_scene'] == 'ck_stop':
					self.scene_stop.encode(struct,self);
				if struct['ck_scene'] == 'ck_open':
					self.scene_open.encode(struct,self);
				if struct['ck_scene'] == 'ck_close':
					self.scene_close.encode(struct,self);
				if struct['ck_scene'] == 'ck_prompt':
					self.scene_prompt.encode(struct,self);
				if struct['ck_scene'] == 'ck_able':
					self.scene_able.encode(struct,self);
				if struct['ck_scene'] == 'ck_del':
					self.scene_del.encode(struct,self);
				if struct['ck_scene'] == 'ck_madd':
					self.scene_madd.encode(struct,self);
				if struct['ck_scene'] == 'ck_mo_time':
					self.scene_time.encode(struct,self);
				if struct['ck_scene'] == 'ck_cbell':
					self.scene_bell.encode(struct,self);
				if struct['ck_scene'] == 'ck_sbell':
					self.scene_sbell.encode(struct,self);
			else:
				msg_id = SceneParam._get_random_id(len(msg));
				struct['result']['msg'] = msg[msg_id];
			if struct.has_key('step') and struct['step'] == 'end':
				del struct['ck_scene'];
				del struct['step']
			struct['mcks'] = self.clocks;
			SceneParam._degbu_info(struct);
			self._tail(struct);
		except Exception as e:
			if struct.has_key('step'): del struct['step']
			if struct.has_key('ck_scene'): del struct['ck_scene'];
			msg_id = SceneParam._get_random_id(len(err_msg));
			struct['result']['msg'] = err_msg[msg_id];
			raise MyException(format(e));
