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
				os.path.join(abspath,'tdata','some_noun','some_noun_person.json'), #人物名称
				os.path.join(abspath,'tdata','some_noun','some_noun_pname.json'), #人物名称
				os.path.join(abspath,'tdata','some_noun','some_noun_place.json'),#地点名称
				os.path.join(abspath,'tdata','some_noun','some_noun_sth.json'),#事物名称
				os.path.join(abspath,'tdata','some_noun','some_noun_absth.json'), #抽象名词
				os.path.join(abspath,'tdata','some_noun','some_noun_food.json')  #食物名词
			],
			#形容词数据加载地址
			"SomeAdj":[
				os.path.join(abspath,'tdata','some_adj','some_adj_abstract.json'),
				os.path.join(abspath,'tdata','some_adj','some_adj_appear.json'),
				os.path.join(abspath,'tdata','some_adj','some_adj_feel.json'),
				os.path.join(abspath,'tdata','some_adj','some_adj_level.json')
			],
			#动词数据加载地址
			"SomeVerb":[
				os.path.join(abspath,'tdata','some_verb','some_verb_tend.json'),#趋向动词
				os.path.join(abspath,'tdata','some_verb','some_verb_can.json'),#能愿动词
				os.path.join(abspath,'tdata','some_verb','some_verb_pycho.json'),#心理动词
				os.path.join(abspath,'tdata','some_verb','some_verb_xi.json'),#判定动词
				os.path.join(abspath,'tdata','some_verb','some_verb_irre.json'),#不规则动词
				os.path.join(abspath,'tdata','some_verb','some_verb_let.json'),#LET 动词
				os.path.join(abspath,'tdata','some_verb','some_verb_call.json'),#CALL 动词
				os.path.join(abspath,'tdata','some_verb','some_verb_do.json'),#DO 动词
				os.path.join(abspath,'tdata','some_verb','some_verb_action.json') #ACTION 动词
			],
			#代词数据加载地址
			"SomePronoun":[
				os.path.join(abspath,'tdata','some_pron','some_pron_person.json'),#人称代词
				os.path.join(abspath,'tdata','some_pron','some_pron_logic.json'),#逻辑代词
				os.path.join(abspath,'tdata','some_pron','some_pron_question.json'),#疑问代词
				os.path.join(abspath,'tdata','some_pron','some_pron_specify.json') #相对代词
			],
			#介词数据加载地址
			"SomePrep":os.path.join(abspath,'tdata','some_prep','some_prep.json'),
			#副词数据加载地址
			"SomeAdverb":[
				os.path.join(abspath,'tdata','some_adverb','some_adverb_level.json'),#程度副词
				os.path.join(abspath,'tdata','some_adverb','some_adverb_time.json'),#时间副词
				os.path.join(abspath,'tdata','some_adverb','some_adverb_dect.json'),#判定副词
				os.path.join(abspath,'tdata','some_adverb','some_adverb_scope.json'),#范围副词
				os.path.join(abspath,'tdata','some_adverb','some_adverb_rate.json'),#频率副词
				os.path.join(abspath,'tdata','some_adverb','some_adverb_mood.json') #情态副词
			],
			#助词数据加载地址
			"SomeAux":[
				os.path.join(abspath,'tdata','some_aux','some_auxj.json')#结构助词
			],
			"SomeSpace":os.path.join(abspath,'tdata','some_pspace.json'),
			"SomeUnits":os.path.join(abspath,'tdata','some_unit','some_unit.json'),
			"SomeNums":os.path.join(abspath,'tdata','some_num.json'),
			"SomeTmood":os.path.join(abspath,'tdata','some_tmood.json'),
			"SomeOther":os.path.join(abspath,'tdata','some_other','some_other.json')
		}
		self.data = {
			"SomeAdj":dict(),
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
