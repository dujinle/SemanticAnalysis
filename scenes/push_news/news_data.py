#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,random
from common import logging
from myexception import MyException
from com_base import ComBase as NewsBase

#处理新闻场景
class NewsData(NewsBase):

	#新闻数据中根据标题模糊匹配数据
	def get_news_by_title(self,title):
		for data in self.data:
			item = self.data[data];
			for ni in item:
				if ni['title'].find(title) <> -1:
					return ni;

	#随机获取指定板块的几条新闻数据
	def get_news_by_plate(self,plate,n):
		if not self.data.has_key(plate): return None;
		item = self.data[plate];
		if len(item) >= n: return item[:n];
		return item;

	def get_news_by_random(self,n):
		plate = self.data.keys();
		nlist = list();
		while True:
			if n <= 0: break;
			idx = random.randint(0,len(plate));
			if idx >= len(plate): idx = idx - 1;
			items = self.data[plate[idx]];
			nidx = random.randint(0,len(items));
			if nidx == len(items): nidx = nidx - 1;
			nlist.append(items[nidx]);
			n = n - 1;
		return nlist;
