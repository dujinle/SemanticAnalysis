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
			ret['inlist'] = sres['inlist'];
			if mdl == 'Timer':
				if sres.has_key('taglist'):
					ret['taglist'] = list();
					for tag in sres['taglist']:
						if tag.has_key('interval'):
							tdic = dict();
							tdic['strs'] = ''
							for tm in tag['times']:
								tdic['strs'] = tdic['strs'] + tm['value'];
							start = tag['interval'][0];
							end = tag['interval'][1];
							tdic['interval'] = list();
							tdic['interval'].append('-'.join([str(i) for i in start]));
							tdic['interval'].append('-'.join([str(i) for i in end]));
							ret['taglist'].append(tdic);
						elif tag['type'].find('mood_') <> -1:
							ret['taglist'].append(tag);
			elif mdl == 'Local':
				if sres.has_key('locals'):
					ret['locals'] = sres['locals'];
			elif mdl == 'Music':
				if sres.has_key('music'):
					ret['music'] = sres['music'];
			elif mdl == 'Catering':
				if sres.has_key('catering'):
					ret['catering'] = sres['catering'];
			elif mdl == 'Flight' or mdl == 'Alarm':
				ret = sres;
				#ret['flight'] = sres['flight'];
			else:
				ret['value'] = sres['value'];
				ret['dir'] = sres['dir'];
			self.write(self.gen_result(0,'enjoy success',ret));
		except MyException as e:
			self.except_handle(e.value);
			return;
