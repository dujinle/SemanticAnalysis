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
			"SomeNouns":[
				os.path.join(abspath,'tdata','some_nouns','some_noun_concept.json'),#人物名称
				os.path.join(abspath,'tdata','some_nouns','some_noun_person.json'), #人物名称
				os.path.join(abspath,'tdata','some_nouns','some_noun_subject.json') #地点名称
			],
			#情态词加载地址
			"SomeMoods":[
				os.path.join(abspath,'tdata','some_moods','some_mood_jds.json')
			],
			#动词数据加载地址
			"SomeVerbs":[
				os.path.join(abspath,'tdata','some_verbs','some_verb_basic.json'),
				os.path.join(abspath,'tdata','some_verbs','some_verb_logic.json')
			],
			#代词数据加载地址
			"SomeProns":[
				os.path.join(abspath,'tdata','some_prons','some_prons.json')
			],
			#逻辑词加载地址
			"SomeLogics":[
				os.path.join(abspath,'tdata','some_logics','some_logic_poss.json'),
				os.path.join(abspath,'tdata','some_logics','some_logic_terms.json'),
				os.path.join(abspath,'tdata','some_logics','some_logic_times.json')
			],
			#助词数据加载地址
			"SomeAuxs":[
				os.path.join(abspath,'tdata','some_auxs','some_auxs.json')#结构助词
			],
			#时态词加载地址
			"SomeTenses":[
				os.path.join(abspath,'tdata','some_tenses','some_tenses.json')
			],
			#量词加载地址
			"SomeNunit":[
				os.path.join(abspath,'tdata','some_nunit','some_nunit.json')
			],
		}
		self.data = {
			"SomeVerbs":dict(),
			"SomeNouns":dict(),
			"SomeProns":dict(),
			"SomeAuxs":dict(),
			"SomeMoods":dict(),
			"SomeTenses":dict(),
			"SomeLogics":dict(),
			"SomeNunit":dict()
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
