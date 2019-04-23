import sqlite3 as lite

dbname = 'humidityTemp_data.db'

def del_tabdata():
	conn=lite.connect(dbname)
	curs=conn.cursor()
	curs.execute("DELETE FROM DHT_data")
	conn.commit()
	conn.close()

del_tabdata()
