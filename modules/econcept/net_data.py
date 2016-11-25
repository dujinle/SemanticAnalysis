#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,json,os,common
from myexception import MyException
abspath = os.path.dirname(__file__);

#story all the data net info
class NetData():
	def __init__(self):
		self.dfiles = {
			"Adjs":os.path.join(abspath,'tdata','adj_dic.json'),
			"Verbs":os.path.join(abspath,'tdata','verb_dic.json'),
			"SomeBody":os.path.join(abspath,'tdata','some_body.json'),
			"SomePlace":os.path.join(abspath,'tdata','some_place.json'),
			"SomeThing":os.path.join(abspath,'tdata','some_thing.json'),
			"PlaceSpace":os.path.join(abspath,'tdata','place_space.json'),
			"Bpronoun":os.path.join(abspath,'tdata','body_pronoun.json'),
			"Lpronoun":os.path.join(abspath,'tdata','logical_pronoun.json')
		}
		self.data = {
			"Adjs":None,
			"Verbs":None,
			"SomeBody":None,
			"SomePlace":None,
			"SomeThing":None,
			"PlaceSpace":None,
			"Bpronoun":None,
			"Lpronoun":None
		}

	def get_data_key(self,key):
		if self.data.has_key(key):
			return self.data[key];
		return None;

	def load_data(self):
		for key in self.data.keys():
			dfile = self.dfiles[key];
			self.data[key] = common.read_json(dfile);
