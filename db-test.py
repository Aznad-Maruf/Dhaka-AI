import sqlite3
from passlib.hash import sha256_crypt

#passw = sha256_crypt.hash("abc")
#print sha256_crypt.verify("abc", passw)
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
conn.execute('insert into Team values ("admin","%s","a@b.com",1,1,0)'%sha256_crypt.hash("admin"))
#print "Opened database successfully";
#conn.execute('insert into Team values ("p","s","d",2,45,66)')
#cursor= conn.execute('select * from Team')
#for row in cursor:
#    print row
#print cursor.fetchone()==None
conn.commit()
conn.close()
