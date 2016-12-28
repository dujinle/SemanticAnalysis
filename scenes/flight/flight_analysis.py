#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from com_base import ComBase as FlightBase
import com_funcs as ComFuncs

#处理 航班信息
class FlightAnalysis(FlightBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into Flight analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			if struct['step'] == 'start':
				if func == 'ctc_flight':
					self._get_ctc_flight(struct,super_b);
					struct['step'] = 'select';
					return None;
			elif struct['step'] == 'select':
				if func == 'book_flight':
					self._book_flight(struct,super_b);
				elif func == 'book':
					self._book_flight_or_hotel(struct,super_b);
				if struct['step'] <> 'select': return None;
			elif struct['step'] == 'if_book_hotel':
				if func == 'book_hotel':
					self._get_hotel_info(struct,super_b);
					struct['step'] = 'select';
					return None;
			elif struct['step'] == 'book_sure':
				self._book_hotel(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());

	def _get_ctc_flight(self,struct,super_b):
		tdic = dict();
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['stype'] == 'CITY':
				if not tdic.has_key('start'): tdic['start'] = item['str'];
				elif not tdic.has_key('end'): tdic['end'] = item['str'];
			elif item.has_key('child') and item['stype'] == 'FLY':
				if not tdic.has_key('end'): tdic['end'] = item['child']['str'];

		flight = super_b.get_flight_info(tdic);
		if flight is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			ComFuncs._set_msg(struct,self.data['msg']['flight']);
		return None;

	def _book_flight(self,struct,super_b):
		time = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['stype'] == 'TIME':
				time = item;
				break;
		if time is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			flight = super_b.get_flight(time);
			if flight is None:
				ComFuncs._set_msg(struct,self.data['msg']['unknow']);
			else:
				struct['result']['book'] = flight;
				ComFuncs._set_msg(struct,self.data['msg']['book_succ']);

	def _get_hotel_info(self,struct,super_b):
		level = addr = None;
		tdic = dict();
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			while True:
				if item['stype'] == 'HOTEL':
					if item.has_key('belong'):
						addr = item['belong'];
					if item.has_key('num'):
						level = item['num'];
				if item.has_key('child'):
					item = item['child'];
				else:
					break;
		hotel = super_b.get_hotel(addr,level);
		if hotel is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['hotel'] = hotel;
			ComFuncs._set_msg(struct,self.data['msg']['hotel_select']);
		return None;

	def _book_flight_or_hotel(self,struct,super_b):
		if super_b.history == 'Flight':
			self._book_flight(struct,super_b);
		elif super_b.history == 'Hotel':
			ComFuncs._set_msg(struct,self.data['msg']['hotel_pnum']);
			struct['step'] = 'book_sure';
		return None;

	def _book_hotel(self,struct,super_b):
		pls = days = None;
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item['stype'] == 'PEOPLE':
				if item.has_key('num'):
					num = item['num'];
					if num.has_key('stc'):
						pls = num['stc'][0]['stype'];
					else:
						pls = num['stype'];
			elif item['stype'] == 'STAY':
				if item.has_key('num'):
					ds = item['num'];
					if ds.has_key('stc'):
						days = ds['stc'][0]['stype'];
		if pls is None or days is None:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		else:
			struct['result']['hotel'] = {'pl':pls,'days':days};
			ComFuncs._set_msg(struct,self.data['msg']['hotel_succ']);
