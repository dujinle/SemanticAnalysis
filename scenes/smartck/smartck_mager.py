#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
import pgsql,collections
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

from common import logging
from myexception import MyException
from scene_mager import SceneMager
import com_funcs as SceneCommon
import smartck_common as SmartckCom

from smartck_dist import SmartckDist
from smartck_data import SmartckData
from smartck_add import SmartckAdd
from smartck_getup import SmartckGetup
from smartck_agenda import SmartckAgenda
from smartck_search import SmartckSearch
from smartck_delay import SmartckDelay
from smartck_stop import SmartckStop
from smartck_open import SmartckOpen
from smartck_close import SmartckClose
from smartck_prompt import SmartckPrompt
from smartck_able import SmartckAble
from smartck_del import SmartckDel
from smartck_madd import SmartckMadd
from smartck_time import SmartckTime
from smartck_bell import SmartckBell
from smartck_sbell import SmartckSBell

class SmartckMager(SceneMager):
	def __init__(self):
		self.tag_objs = list();
		self.dfiles = [
			os.path.join(base_path,'tdata','smartck_add.txt'),
			os.path.join(base_path,'tdata','smartck_getup.txt'),
			os.path.join(base_path,'tdata','smartck_agenda.txt'),
			os.path.join(base_path,'tdata','smartck_search.txt'),
			os.path.join(base_path,'tdata','smartck_delay.txt'),
			os.path.join(base_path,'tdata','smartck_stop.txt'),
			os.path.join(base_path,'tdata','smartck_open.txt'),
			os.path.join(base_path,'tdata','smartck_close.txt'),
			os.path.join(base_path,'tdata','smartck_prompt.txt'),
			os.path.join(base_path,'tdata','smartck_able.txt'),
			os.path.join(base_path,'tdata','smartck_del.txt'),
			os.path.join(base_path,'tdata','smartck_madd.txt'),
			os.path.join(base_path,'tdata','smartck_time.txt'),
			os.path.join(base_path,'tdata','smartck_bell.txt'),
			os.path.join(base_path,'tdata','smartck_sbell.txt'),
			os.path.join(base_path,'tdata','smartck_dist.txt'),
			os.path.join(base_path,'tdata','smartck_data.txt')
		];

		self.fdata = SmartckData();
		self.smartck_dist = SmartckDist();

		self.tag_objs.append(SmartckAdd());
		self.tag_objs.append(SmartckGetup());
		self.tag_objs.append(SmartckAgenda());
		self.tag_objs.append(SmartckSearch());
		self.tag_objs.append(SmartckDelay());
		self.tag_objs.append(SmartckStop());
		self.tag_objs.append(SmartckOpen());
		self.tag_objs.append(SmartckClose());
		self.tag_objs.append(SmartckPrompt());
		self.tag_objs.append(SmartckAble());
		self.tag_objs.append(SmartckDel());
		self.tag_objs.append(SmartckMadd());
		self.tag_objs.append(SmartckTime());
		self.tag_objs.append(SmartckBell());
		self.tag_objs.append(SmartckSBell());
		self.tag_objs.append(self.smartck_dist);
		self.tag_objs.append(self.fdata);

	def _init(self,struct):
		struct['result'] = dict();
		if struct.has_key('ck_name'): del struct['ck_name'];
		if struct.has_key('ck_time'): del struct['ck_time'];
		if struct.has_key('ck_tag'): del struct['ck_tag'];
		if struct.has_key('ttag'): del struct['ttag'];

	def _tail(self,struct):
		if struct.has_key('ck_time'): del struct['ck_time'];
		if struct.has_key('ttag'): del struct['ttag'];
		if struct.has_key('tag'): del struct['tag'];
		if struct.has_key('ck_tag'): del struct['ck_tag'];


	def encode(self,struct):
		try:
			print 'go into alarm scene......';
			self._init(struct);
			self.smartck_dist.dist_encode(struct);

#			'''
			for obj in self.tag_objs:
				obj.encode(struct,self.fdata);
			if not struct.has_key('ck_scene'):
				SceneCommon._set_msg(struct,self.fdata.get_unknow_msg());

			if struct.has_key('step') and struct['step'] == 'end':
				del struct['step'];
				del struct['ck_scene'];
			struct['mcks'] = self.fdata.clocks;
			SmartckCom._degbu_info(struct);
			self._tail(struct);
#			'''
		except Exception as e:
			if struct.has_key('step'): del struct['step']
			if struct.has_key('ck_scene'): del struct['ck_scene'];
			SceneCommon._set_msg(struct,self.fdata.get_err_msg());
			raise MyException(sys.exc_info());
