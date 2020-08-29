import sqlite3
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
conn.execute('update Team set DailyLimit=0 where 1=1')
#print cursor.fetchone()==None
conn.commit()
conn.close()
