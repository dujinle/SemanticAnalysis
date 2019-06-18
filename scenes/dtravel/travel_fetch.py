#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

#处理航班 班次 结构信息 DH2222
class TravelFetch(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into travel fetch......');
			flag = False;
			prev = '';
			for istr in struct['stseg']:
				if not struct['stc'].has_key(istr):
					if flag is True: break;
					else: continue;
				item = struct['stc'][istr];
				if item.has_key('type') and item['type'] == 'ENG':
					flag = True;
					prev = istr;
					continue;
				if flag is True:
					if item.has_key('type') and item['type'] == 'NUM':
						flag = False;
						idx = struct['stseg'].index(istr);
						comb = prev + istr;
						struct['stseg'][idx - 1] = comb;
						struct['stc'][comb] = dict();
						struct['stc'][comb]['str'] = comb;
						struct['stc'][comb]['type'] = 'N',
						struct['stc'][comb]['stype'] = 'FLIGHTNUM';
						del struct['stc'][prev];
						del struct['stc'][istr];
					elif item.has_key('type') and item['type'] == 'NUNIT':
						flag = False;
						idx = struct['stseg'].index(istr);
						comb = prev + istr;
						struct['stseg'][idx - 1] = comb;
						struct['stc'][comb] = dict();
						struct['stc'][comb]['str'] = comb;
						struct['stc'][comb]['type'] = 'N',
						struct['stc'][comb]['stype'] = 'FLIGHTNUM';
						del struct['stc'][prev];
						del struct['stc'][istr];
		except Exception as e:
			raise MyException(sys.exc_info());
