#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from news_base import NewsBase
import news_param as NewParam

#处理新闻场景
class NewsAnalysis(NewsBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into news analysis ......');
			if not struct.has_key('step'): struct['step'] = 'start';
			self._fetch_all_types(struct);

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if not func is None and func == 'get':
					print 'get func:[' + func + ']......';
					self._get_news(struct,super_b);
					struct['step'] = 'which';
					return None;
			elif struct['step'] == 'which':
				if not func is None and func == 'get_info':
					print 'get func:[' + func + ']......';
					self._get_new_by_title(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_all_types(self,struct):
		self._fetch_type(struct,'Objs');
		self._fetch_type(struct,'Sds');
		self._fetch_type(struct,'LocalPrep');
		self._fetch_type(struct,'PerPronom');
		self._fetch_type(struct,'PrepCom');
		self._fetch_type(struct,'VerbCom');

	def _fetch_type(self,struct,key):
		if struct.has_key(key):
			for item in struct[key]: struct[item['str']] = item;
			del struct[key];

	def _fetch_func(self,struct):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			reg = reg + struct[istr]['stype'];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;

	#通过订阅的新闻板块推荐新闻
	def _get_news(self,struct,super_b):
		news_num = self.data['get_num'];
		plates = None;
		nlist = list();
		if struct.has_key('tag'):
			mytag = struct['tag'];
			if mytag.has_key('NEWS'):
				plates = value = mytag['NEWS']['value'];
				n = news_num // len(value);
				for plate in plates:
					news = super_b.get_news_by_plate(plate,n);
					if not news is None:
						for it in news: nlist.append(it);
		else:
			nlist = super_b.get_news_by_random(news_num);
		if nlist is None:
			NewParam._set_msg(struct,self.data['msg']['no_news']);
			return None;
		idx = 1;
		new_titles = '';
		for it in nlist:
			new_titles = new_titles + str(idx) + it['title'];
			idx = idx + 1;
		if plates is None:
			NewParam._set_msg(struct,self.data['msg']['get_news_info'],'',len(nlist),new_titles);
		else:
			NewParam._set_msg(struct,self.data['msg']['get_news_info'],' '.join(plates),len(nlist),new_titles);

	def _get_new_by_title(self,struct,super_b):
		news = None;
		for istr in struct['inlist']:
			news = super_b.get_news_by_title(istr);
			if not news is None:
				break;
		if news is None:
			NewParam._set_msg(struct,self.data['msg']['no_news']);
		else:
			struct['result']['msg'] = news['message'];
		return None;
