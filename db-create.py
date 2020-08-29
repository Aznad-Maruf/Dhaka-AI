import sqlite3

conn = sqlite3.connect('database.db')
print "Opened database successfully";
sql_file = open("schemas.sql")
sql_as_string = sql_file.read()
conn.executescript(sql_as_string)
#conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print "Table created successfully";
conn.commit()
conn.close()