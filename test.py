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
#sys.path.append(os.path.join(base_path,'./location'));
#sys.path.append(os.path.join(base_path,'./flight'));
#sys.path.append(os.path.join(base_path,'./catering'));
#sys.path.append(os.path.join(base_path,'./music'));
#sys.path.append(os.path.join(base_path,'./wordsegs'));
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
		self._clear_struct(self.struct);
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
		klist = struct.keys();
		idx = 0;
		while True:
			if idx >= len(klist): break;
			key = klist[idx];
			if key == 'step' or key == 'scene':
				idx = idx + 1;
				continue;
			else:
				del struct[key];
				del klist[idx];

	def encode(self,text,mdl = None):
		self._clear_struct(self.struct);
		self.struct['text'] = text;
		self.pdeal.encode(self.struct);
		self.struct['otext'] = self.struct['text'];
		self.struct['inlist'] = self.wordseg.tokens(self.struct['text']);
		self.struct['result'] = dict();

		common.print_dic(self.struct);
		self.timer.encode(self.struct);
		self.mytag.encode(self.struct);
		self.concpt.encode(self.struct);
		self.fetch.encode(self.struct);
		return self.struct;

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'Usage: %s tfile' %sys.argv[0];
		sys.exit(-1);

	try:
		mg = Mager();
		mg.init();

		dfile = sys.argv[1];
		dp = open(dfile,'r');
		for line in dp.readlines():
			line = line.strip('\n').decode('utf8');
			if len(line) == 0 or line[0] == '#':
				continue;
			common.print_dic(mg.encode(line,None));
	except Exception as e:
		raise MyException(sys.exc_info());
