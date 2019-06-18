#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
from database import Connect
from commons import common

abspath = os.path.dirname(__file__);

dfiles = {
	#名词对象数据加载地址
	"SomeNouns":[
		os.path.join(abspath,'tdata','some_nouns','some_noun_concept.json'),
		os.path.join(abspath,'tdata','some_nouns','some_noun_person.json'),
		os.path.join(abspath,'tdata','some_nouns','some_noun_subject.json')
	],
	#情态词加载地址
	"SomeMoods":[
		os.path.join(abspath,'tdata','some_moods','some_mood_jing.json'),
		os.path.join(abspath,'tdata','some_moods','some_mood_logic.json')
	],
	#动词数据加载地址
	"SomeVerbs":[
		os.path.join(abspath,'tdata','some_verbs','some_verb_basic.json'),
		os.path.join(abspath,'tdata','some_verbs','some_verb_logic.json')
	],
	#代词数据加载地址
	"SomeProns":[
		os.path.join(abspath,'tdata','some_prons','some_pronp.json')
	],
	#逻辑词加载地址
	"SomeLogics":[
		os.path.join(abspath,'tdata','some_logics','some_logic_pos.json'),
		os.path.join(abspath,'tdata','some_logics','some_logic_term.json'),
		os.path.join(abspath,'tdata','some_logics','some_logic_level.json'),
		os.path.join(abspath,'tdata','some_logics','some_logic_time.json')
	],
	#助词数据加载地址
	"SomeAuxs":[
		os.path.join(abspath,'tdata','some_auxs','some_auxs.json')#结构助词
	],
	#POI地理数据加载地址
	"SomePois":[
		os.path.join(abspath,'tdata','some_pois','some_poi.json')
	],
	#时态词加载地址
	"SomeTenses":[
		os.path.join(abspath,'tdata','some_tenses','some_time_tense.json')
	],
	#量词加载地址
	"SomeNunit":[
		os.path.join(abspath,'tdata','some_nunit','some_nunit.json')
	]
};
data = {
	"SomeVerbs":dict(),
	"SomeNouns":dict(),
	"SomeProns":dict(),
	"SomeAuxs":dict(),
	"SomePois":dict(),
	"SomeMoods":dict(),
	"SomeTenses":dict(),
	"SomeLogics":dict(),
	"SomeNunit":dict()
};

def load_data():
	for key in data.keys():
		dfile = dfiles[key];
		if isinstance(dfile,list):
			for tfile in dfile:
				tdic = common.read_json(tfile);
				if not tdic is None:
					data[key].update(tdic);
		else:
			tdic = common.read_json(dfile);
			if not tdic is None:
				data[key].update(tdic);

if __name__ == '__main__':

	load_data();

	conn = Connect();
	conn.connect('root','root','192.168.102.82','ChinaNet');

	tables = conn.get_tables();
	for table in tables:
		if table.find('system') <> -1: continue;
		print table;
