#by Qian Ma
#used for update the freq field of table newterm

import twitter
import time
import MySQLdb


conn=MySQLdb.connect(host="10.240.119.20",user="root",passwd="cis700fall2014",db="cis700",charset="utf8")
cur = conn.cursor()

while 1:
    temp_time=int(time.time())
    cur.execute('UPDATE newterm SET freq=count*60.6*60/(%s-time)', temp_time)
    conn.commit()
    time.sleep(300) #period is 5min


cur.close()
conn.close()





