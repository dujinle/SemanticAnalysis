#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import collections

#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'./commons'));

sys.path.append(os.path.join(base_path,'./scenes'));
sys.path.append(os.path.join(base_path,'./scenes/math'));
sys.path.append(os.path.join(base_path,'./scenes/dmusic'));
sys.path.append(os.path.join(base_path,'./scenes/flight'));
sys.path.append(os.path.join(base_path,'./scenes/calendar'));
sys.path.append(os.path.join(base_path,'./scenes/foodspot'));
sys.path.append(os.path.join(base_path,'./scenes/shopping'));
sys.path.append(os.path.join(base_path,'./scenes/traffic'));
sys.path.append(os.path.join(base_path,'./scenes/push_news'));
sys.path.append(os.path.join(base_path,'./scenes/navigation'));
sys.path.append(os.path.join(base_path,'./scenes/on_off_line'));
sys.path.append(os.path.join(base_path,'./scenes/translation'));
sys.path.append(os.path.join(base_path,'./scenes/bvoice/pystr'));
sys.path.append(os.path.join(base_path,'./scenes/send_message'));

sys.path.append(os.path.join(base_path,'./scenes/alarm_clock/pystr'));
sys.path.append(os.path.join(base_path,'./scenes/ctemperature/pystr'));

sys.path.append(os.path.join(base_path,'./modules/timer'));
sys.path.append(os.path.join(base_path,'./modules/mytag'));
sys.path.append(os.path.join(base_path,'./modules/wordsegs'));
sys.path.append(os.path.join(base_path,'./modules/prev_deal'));
sys.path.append(os.path.join(base_path,'./modules/econcept'));
sys.path.append(os.path.join(base_path,'./modules/fetch_stc'));
sys.path.append(os.path.join(base_path,'./modules/dist_scene'));
sys.path.append(os.path.join(base_path,'./modules/pronom_prep'));
#==============================================================

import common,config
from myexception import MyException
from scene_cmager import SceneMager
from news_mager import NewsMager
from guide_mager import GuideMager
from music_mager import MusicMager
from voice_mager import VoiceMager
from phone_mager import PhoneMager
from cal_mager import CalMager
from trans_mager import TransMager
from math_mager import MathMager
from food_mager import FoodMager
from shop_mager import ShopMager
from nav_mager import NavMager
from temp_mager import TempMager
from flight_mager import FlightMager
from o2o_mager import O2oMager

from time_cmager import TimeMager
from tag_cmager import MytagMager
from pdeal_cmager import PDealMager
from con_mager import ConMager
from fetch_mager import FetchMager
from dist_mager import DistMager

from wordseg import WordSeg

class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.timer = TimeMager();
		self.mytag = MytagMager();
		self.pdeal = PDealMager();
		self.concpt = ConMager();
		self.fetch = FetchMager();
		self.dist = DistMager();

		self.struct = collections.OrderedDict();

		self.modules = dict();
		self.modules['Voice'] = VoiceMager();
		self.modules['Temp'] = TempMager();
		self.modules['Alarm'] = SceneMager();
		self.modules['News'] = NewsMager();
		self.modules['Traffic'] = GuideMager();
		self.modules['Music'] = MusicMager();
		self.modules['Phone'] = PhoneMager();
		self.modules['Calendar'] = CalMager();
		self.modules['Trans'] = TransMager();
		self.modules['Math'] = MathMager();
		self.modules['Food'] = FoodMager();
		self.modules['Shop'] = ShopMager();
		self.modules['Nav'] = NavMager();
		self.modules['Flight'] = FlightMager();
		self.modules['O2O'] = O2oMager();

	def set_step(self,step): self.struct['step'] = step;
	def set_scene(self,scene):
		common.print_dic(self.struct);
		self.struct['scene'] = scene;

	def init(self):
		try:
			self.timer.init('Timer');
			self.mytag.init('Mytag');
			self.pdeal.init('PDeal');
			self.concpt.init('Concept');
			self.fetch.init('Fetch');
			self.dist.init('Dist');
			for key in self.modules:
				self.modules[key].init(key);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _clear_struct(self,struct):
		idx = 0;
		while True:
			if idx >= len(struct.keys()): break;
			key = struct.keys()[idx];
			if key == 'step' or key == 'scene':
				idx = idx + 1;
				continue;
			else:
				del struct[key];
				continue;

	def encode(self,text,mdl = None):
		self._clear_struct(self.struct);
		self.struct['text'] = text;
		self.pdeal.encode(self.struct);
		self.struct['otext'] = self.struct['text'];
		self.struct['inlist'] = self.wordseg.tokens(self.struct['text']);
		self.struct['result'] = dict();

		self.timer.encode(self.struct);
		self.mytag.encode(self.struct);
		self.concpt.encode(self.struct);
#		common.print_dic(self.struct);
		self.fetch.encode(self.struct);
		if not self.struct.has_key('scene'):
			self.dist.encode(self.struct);
		if self.struct.has_key('scene'):
			mdl = self.struct['scene'];
		if self.modules.has_key(mdl):
			self.struct['text'] = self.struct['otext'];
			mobj = self.modules[mdl];
			mobj.encode(self.struct);
		if self.struct.has_key('step') and self.struct['step'] == 'end':
			del self.struct['scene'];
			del self.struct['step'];
		return self.struct;

#'''
try:
	mg = Mager();
	mg.init();
#	common.print_dic(mg.encode(u'7点半叫我起床',None));
#	common.print_dic(mg.encode(u'好啦，受不了真恶心，我起来啦！','Alarm'));
#	common.print_dic(mg.encode(u'哦，对了提醒下我9点半打个电话给老张',None));
#	common.print_dic(mg.encode(u'小秘，有什么新闻','News'));
#	common.print_dic(mg.encode(u'有什么新闻','News'));
#	common.print_dic(mg.encode(u'哟，又吹牛啦！国足那条',None));
	common.print_dic(mg.encode(u'小秘我现在出门去公司了',None));
#	common.print_dic(mg.encode(u'太太喜欢的音乐',None));
#	common.print_dic(mg.encode(u'小秘我最爱的音乐','Music'));
#	common.print_dic(mg.encode(u'小秘停停停，有什么新歌能听的','Music'));
#	common.print_dic(mg.encode(u'小秘，下一首','Music'));
#	common.print_dic(mg.encode(u'小秘，给太太电话','Phone'));
#	common.print_dic(mg.encode(u'小秘，今天几号','Calendar'));
#	common.print_dic(mg.encode(u'英文翻译，nice','Trans'));
#	common.print_dic(mg.encode(u'小秘，175乘以8等于多少','Math'));
#	common.print_dic(mg.encode(u'公司附近美食推荐','Food'));
#	common.print_dic(mg.encode(u'去过啦不好吃，有什么别的推荐','Food'));
#	common.print_dic(mg.encode(u'1点10分，6人，安静',None));
#	common.print_dic(mg.encode(u'小秘，发个信息给太太，内容是：明天早上的飞机到北京，后天回。下班后我来买菜，您去接宝贝回家。','Phone'));
#	common.print_dic(mg.encode(u'念吧！','Phone'));
#	common.print_dic(mg.encode(u'不用了','Phone'));
#	common.print_dic(mg.encode(u'下午准备想去拜访下客户，顺便想要买点礼物，不知道有什么好推荐的。','Shop'));
#	common.print_dic(mg.encode(u'车辆需要加油','Refuel'));
#	common.print_dic(mg.encode(u'上门拜访联通的肖总','Nav'));
#	common.print_dic(mg.encode(u'后天广州飞北京的航班信息','Flight'));
#	common.print_dic(mg.encode(u'预订10点的，这样我可以吃个早餐','Flight'));
#	common.print_dic(mg.encode(u'当然要定，国贸附近的5星级酒店推荐一下','Flight'));
#	common.print_dic(mg.encode(u'定啊','Flight'));
#	common.print_dic(mg.encode(u'2个人，住10天。',None));
#	common.print_dic(mg.encode(u'明天找人来打扫下家里','O2O'));
#	common.print_dic(mg.encode(u'明天想去打高尔夫',None));
#	common.print_dic(mg.encode(u'周六想约张总去钓鱼。',None));
#	common.print_dic(mg.encode(u'到时候再看',None));
#	common.print_dic(mg.encode(u'明天是宝贝的生日，今年送点什么好？','Shop'));
#	common.print_dic(mg.encode(u'选完了',None));
#	common.print_dic(mg.encode(u'基本不在家，送公司吧',None));
#	common.print_dic(mg.encode(u'买些鹅肝送到家里面，半斤','Shop'));
#	common.print_dic(mg.encode(u'微信语音连线永科','Phone'));
#	common.print_dic(mg.encode(u'打电话','Phone'));
#	common.print_dic(mg.encode(u'重复拨',None));
except Exception as e:
	raise e;
#'''
