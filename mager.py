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
sys.path.append(os.path.join(base_path,'./alarm_clock/pystr'));
sys.path.append(os.path.join(base_path,'./bvoice/pystr'));
sys.path.append(os.path.join(base_path,'./ctemperature/pystr'));

sys.path.append(os.path.join(base_path,'./modules/timer'));
sys.path.append(os.path.join(base_path,'./modules/tmood'));
sys.path.append(os.path.join(base_path,'./modules/mytag'));
sys.path.append(os.path.join(base_path,'./modules/wordsegs'));
sys.path.append(os.path.join(base_path,'./modules/prev_deal'));
sys.path.append(os.path.join(base_path,'./modules/num_unit'));
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
from voice_mager import VoiceMager
from temp_mager import TempMager
from time_cmager import TimeMager
from tag_cmager import MytagMager
from pdeal_cmager import PDealMager
from nunit_mager import NunitMager
from pprep_mager import PPrepMager
from tmood_mager import TMoodMager

from wordseg import WordSeg
#from concept_mager import ConceptMager
#from local_mager import LocalMager
#from music_mager import MusicMager
#from catering_mager import CateringMager
#from flight_mager import FlightMager

class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.timer = TimeMager();
		self.mytag = MytagMager();
		self.pdeal = PDealMager();
		self.nunit = NunitMager();
		self.pprep = PPrepMager();
		self.tmood = TMoodMager();
#		self.concept = ConceptMager();

		self.struct = collections.OrderedDict();

		self.modules = dict();
		self.modules['Voice'] = VoiceMager();
		self.modules['Temp'] = TempMager();
		self.modules['Alarm'] = SceneMager();
#		self.modules['Local'] = LocalMager(self.wordseg);
#		self.modules['Music'] = MusicMager(self.wordseg);
#		self.modules['Catering'] = CateringMager(self.wordseg);
#		self.modules['Flight'] = FlightMager(self.wordseg);

	def init(self):
		try:
			self.timer.init('Timer');
			self.mytag.init('Mytag');
			self.pdeal.init('PDeal');
			self.nunit.init('Nunit');
			self.pprep.init('PrepPronom');
			self.tmood.init('TMood');
			for key in self.modules:
				self.modules[key].init(key);
		except Exception as e:
			raise MyException(sys.exc_info());

	def encode(self,text,mdl = None):

		self.struct['text'] = text;
		self.struct['inlist'] = self.wordseg.tokens(self.struct['text']);
		self.pdeal.encode(self.struct);
		self.tmood.encode(self.struct);
		self.timer.encode(self.struct);
		self.mytag.encode(self.struct);
		self.nunit.encode(self.struct);
		self.pprep.encode(self.struct);
		if mdl is None:
			pass;
	#		mdl = self.concept.encode(struct);
		if self.modules.has_key(mdl):
			mobj = self.modules[mdl];
			mobj.encode(self.struct);
		return self.struct;


#'''
try:
	mg = Mager();
	mg.init();
	#common.print_dic(mg.encode(u'把声音调大点'));
	#common.print_dic(mg.encode(u'把声音调大点'));
	common.print_dic(mg.encode(u'给我一天时间','Alarm'));
except Exception as e:
	raise e;
#'''
