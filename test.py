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
from time_cmager import TimeMager
from tag_cmager import MytagMager
from pdeal_cmager import PDealMager
from con_mager import ConMager

from wordseg import WordSeg

class Mager:
	def __init__(self):
		self.wordseg = WordSeg();
		self.timer = TimeMager();
		self.mytag = MytagMager();
		self.pdeal = PDealMager();
		self.concpt = ConMager();

		self.struct = collections.OrderedDict();

		self.modules = dict();

	def init(self):
		try:
			self.timer.init('Timer');
			self.mytag.init('Mytag');
			self.pdeal.init('PDeal');
			self.concpt.init('Concept');
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

		self.timer.encode(self.struct);
		self.mytag.encode(self.struct);
		self.concpt.encode(self.struct);
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
			line = line.strip('\n').strip('\r').decode('utf8');
			if len(line) == 0 or line[0] == '#':
				continue;
			common.print_dic(mg.encode(line,None));
	except Exception as e:
		raise MyException(sys.exc_info());
