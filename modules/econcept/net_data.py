#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,json,os,common
from myexception import MyException
abspath = os.path.dirname(__file__);

#story all the data net info
class NetData():
	def __init__(self):
		self.dfiles = {
			#名词对象数据加载地址
			"SomeObjs":[
				os.path.join(abspath,'tdata','some_objb.json'), #人物名称
				os.path.join(abspath,'tdata','some_objp.json'),#地点名称
				os.path.join(abspath,'tdata','some_objt.json'),#事物名称
				os.path.join(abspath,'tdata','some_obja.json')  #抽象名词
			],
			#形容词数据加载地址
			"SomeAdjs":os.path.join(abspath,'tdata','some_adj.json'),
			#动词数据加载地址
			"SomeVerb":[
				os.path.join(abspath,'tdata','some_verbx.json'),#判定动词
				os.path.join(abspath,'tdata','some_verbi.json'),#不规则动词
				os.path.join(abspath,'tdata','some_verbt.json'),#趋向动词
				os.path.join(abspath,'tdata','some_verbl.json'),#LET 动词
				os.path.join(abspath,'tdata','some_verbd.json'),#DO 动词
				os.path.join(abspath,'tdata','some_verbc.json'),#CALL 动词
				os.path.join(abspath,'tdata','some_verbm.json'),#能愿动词
				os.path.join(abspath,'tdata','some_verbp.json'),#心理动词
				os.path.join(abspath,'tdata','some_verba.json') #ACTION 动词
			],
			#代词数据加载地址
			"SomePronoun":[
				os.path.join(abspath,'tdata','some_pronb.json'),#人称代词
				os.path.join(abspath,'tdata','some_pronl.json'),#逻辑代词
				os.path.join(abspath,'tdata','some_pronq.json'),#疑问代词
				os.path.join(abspath,'tdata','some_pronx.json') #相对代词
			],
			#介词数据加载地址
			"SomePrep":os.path.join(abspath,'tdata','some_prep.json'),
			#副词数据加载地址
			"SomeAdverb":[
				os.path.join(abspath,'tdata','some_adverbl.json'),#程度副词
				os.path.join(abspath,'tdata','some_adverbt.json'),#时间副词
				os.path.join(abspath,'tdata','some_adverbd.json'),#判定副词
				os.path.join(abspath,'tdata','some_adverbs.json'),#范围副词
				os.path.join(abspath,'tdata','some_adverbr.json'),#频率副词
				os.path.join(abspath,'tdata','some_adverbq.json') #情态副词
			],
			#助词数据加载地址
			"SomeAux":[
				os.path.join(abspath,'tdata','some_auxj.json')#结构助词
			],
			"SomeSpace":os.path.join(abspath,'tdata','some_pspace.json'),
			"SomeUnits":os.path.join(abspath,'tdata','some_unit.json'),
			"SomeNums":os.path.join(abspath,'tdata','some_num.json'),
			"SomeTmood":os.path.join(abspath,'tdata','some_tmood.json'),
			"SomeOther":os.path.join(abspath,'tdata','some_other.json')
		}
		self.data = {
			"SomeAdjs":dict(),
			"SomeVerb":dict(),
			"SomeObjs":dict(),
			"SomeSpace":dict(),
			"SomePronoun":dict(),
			"SomeAdverb":dict(),
			"SomeUnits":dict(),
			"SomeNums":dict(),
			"SomeAux":dict(),
			"SomePrep":dict(),
			"SomeTmood":dict(),
			"SomeOther":dict()
		}

	def get_data_key(self,key):
		if self.data.has_key(key):
			return self.data[key];
		return None;

	def load_data(self):
		for key in self.data.keys():
			dfile = self.dfiles[key];
			if isinstance(dfile,list):
				for tfile in dfile:
					tdic = common.read_json(tfile);
					if not tdic is None:
						self.data[key].update(tdic);
			else:
				tdic = common.read_json(dfile);
				if not tdic is None:
					self.data[key].update(tdic);
