#by Qian Ma
#initialize the database, define the fields and keys of tables

import twitter
import MySQLdb


conn=MySQLdb.connect(host="10.240.119.20",user="root",passwd="cis700fall2014")
cur = conn.cursor()

cur.execute('create database cis700 default charset utf8 COLLATE utf8_bin')
conn.select_db('cis700')

cur.execute('create table tweets(id varchar(20), time int, user varchar(20), content text binary, primary key(id))')
cur.execute('create table newterm(word varchar(140) binary, count int, time int, freq float , analyzed_time int, primary key(word))')
cur.execute('create table tweets_newterm(id varchar(20), word varchar(140) binary, primary key(id, word))')
cur.execute('create table vocabulary(term varchar(140) binary, key(term))')

conn.commit()


cur.close()
conn.close()





