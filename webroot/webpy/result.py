#!/usr/bin/python
#-*- coding : utf-8 -*-

import sys,os
#=============================================
''' import common module '''
base_path = os.path.dirname(__file__);
sys.path.append(base_path + '/../../commons');
#=============================================

import tornado.web
from logger import *
import common
from handler import RequestHandler
from myexception import MyException

class ResultHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.json_loads_body
	def post(self):
		try:
			if not self.body_json.has_key('text'):
				self.except_handle('the url data format error');
				return ;
			if not self.body_json.has_key('mdl'):
				self.except_handle('not found argumen mdl');
				return ;
			mdl = self.body_json['mdl'];
			itest = self.body_json['text'];
			if len(itest) == 0:
				self.except_handle('the param text is empty');
				return ;
			logging.info('mdl:%s input:%s' %(mdl,itest));
			mager = self.get_mager();
			sres = mager.encode(itest,mdl);
			ret = dict();
			ret['text'] = sres['text'];
			ret['inlist'] = sres.get('inlist');

			if mdl == 'Timer':
				ret['result'] = list();
				if sres.has_key('intervals') and len(sres['intervals']) > 0:
					for tag in sres['intervals']:
						tdic = dict();
						tdic['strs'] = tag['str'];
						start = tag['start'];
						end = tag['end'];
						tdic['interval'] = list();
						tdic['interval'].append('-'.join([str(i) for i in start]));
						tdic['interval'].append('-'.join([str(i) for i in end]));
						ret['result'].append(tdic);
				elif sres.has_key('mood') and len(sres['mood']) > 0:
					ret['result'].append(sres['mood']);
			elif mdl == 'Local':
				if sres.has_key('locals'):
					ret['locals'] = sres['locals'];
			elif mdl == 'Music':
				if sres.has_key('music'):
					ret['music'] = sres['music'];
			elif mdl == 'Catering':
				if sres.has_key('catering'):
					ret['catering'] = sres['catering'];
			elif mdl == 'Alarm':
				common.print_dic(sres);
				if sres.has_key('result'): ret = sres['result'];
				else: ret = sres;
			elif mdl == 'Flight':
				ret = sres;
			else:
				ret['value'] = sres['value'];
				ret['dir'] = sres['dir'];
			self.write(self.gen_result(0,'enjoy success',ret));
		except MyException as e:
			self.except_handle(e.value);
			return;
