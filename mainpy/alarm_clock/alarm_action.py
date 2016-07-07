#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,alarm_common
from myexception import MyException
from base import Base

class AA(Base):

	def encode(self,struct):
		try:
			intext = struct['text'];
			rlist = alarm_common._if_has_key(intext,self.data['keys']);
			regs = self.data['regs'];
			for key in rlist:
				self._match_reg(struct,key);
		except MyException as e: raise e;

	def _match_reg(self,struct,key):
		if not struct.has_key('clocks'): struct['clocks'] = list();
		text = struct['text'];
		regs = self.data['regs'];
		matchs = dict();
		tregs = dict();
		for reg in regs:
			regtr = '|'.join(reg['same']);
			if regtr.find(key) == -1: continue;
			comp = re.compile(regtr);
			match = comp.search(text);
			if match is None: continue;
			matchs[key] = match;
			tregs[key] = reg;
		if len(matchs) == 0: return None;
		mykey = alarm_common._make_only_one(matchs);
		match = matchs[mykey];
		reg = tregs[mykey];

		tmat = match.group(0);
		idx = alarm_common._find_idx(text,tmat,'null');
		tdic = copy.deepcopy(reg);
		tdic['value'] = tmat;
		struct['clocks'].insert(idx,tdic);
		struct['text'] = text.replace(tdic['value'],'AA',1);
