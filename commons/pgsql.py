#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,json
import psycopg2

#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(base_path);

#============================================
from logger import *
p_conn = None;
def pg_conncet(dbname='mytag',user='postgres',password='123456',host='172.17.42.1',port='5432'):
	global p_conn;
	if p_conn is None:
		#p_conn = psycopg2.connect(dbname,user,password,host,port);
		p_conn = psycopg2.connect(dbname='mytag',user='postgres',password='123456',host='172.17.0.11',port='5432');
	return p_conn;

def pg_cursor(conn): return conn.cursor();

def pg_query(cursor,sql,params): return cursor.execute(sql,params);

def pg_commit(conn): conn.commit();

def pg_close_cursor(cur): cur.close();

def pg_close_conn(conn):
	conn.close();
	conn = None;

def pg_rollback(conn): conn.rollback();
