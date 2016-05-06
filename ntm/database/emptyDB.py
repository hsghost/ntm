#by Qian Ma
#empty the database

import MySQLdb

conn=MySQLdb.connect(host="10.240.119.20",user="root",passwd="cis700fall2014",db="cis700",charset="utf8")
cur = conn.cursor()

cur.execute('delete from tweets')
cur.execute('delete from tweets_newterm')
cur.execute('delete from newterm')
cur.execute('delete from vocabulary')

conn.commit()

cur.close()
conn.close()





