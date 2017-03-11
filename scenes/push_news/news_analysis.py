#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from com_base import ComBase as NewsBase
import news_param as NewParam

#处理新闻场景
class NewsAnalysis(NewsBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into news analysis ......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if not func is None and func == 'get':
					self._get_news(struct,super_b);
					struct['step'] = 'which';
					return None;
			elif struct['step'] == 'which':
				if not func is None and func == 'get_info':
					self._get_new_by_title(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	#通过订阅的新闻板块推荐新闻
	def _get_news(self,struct,super_b):
		news_num = self.data['get_num'];
		plates = None;
		nlist = list();
		if struct.has_key('tag') and struct['tag'].has_key('NEWS'):
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
