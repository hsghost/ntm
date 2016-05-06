#by Qian Ma
#used together with linux alias for quickly reviewing the data in database

if __name__ == "__main__":

	import MySQLdb
	import sys

	conn=MySQLdb.connect(host="10.240.119.20",user="root",passwd="cis700fall2014",db="cis700",charset="utf8")
	cur = conn.cursor()

	count=0
	if len(sys.argv)==2:
		if sys.argv[1]=='t':
			count=cur.execute('select * from tweets')
		if sys.argv[1]=='r':
                	count=cur.execute('select * from tweets_newterm')
		if sys.argv[1]=='n':
                	count=cur.execute('select * from newterm')
		if sys.argv[1]=='v':
                	count=cur.execute('select * from vocabulary')

        elif len(sys.argv)==3:
		if sys.argv[1]=='n':
			count=cur.execute('select * from newterm where count>=%s', sys.argv[2])

        elif len(sys.argv)==4:
                if sys.argv[1]=='n' and sys.argv[2]=='top':
                        count=cur.execute('select * from newterm where count>=10 order by freq desc limit 0, %s', eval(sys.argv[3]))
	conn.commit()

	result=cur.fetchall()

	cur.close()
	conn.close()

	for r in result:
		print r

	print
	print 'count =',count
	print



