import sqlite3
conn=sqlite3.connect('humidityTemp_data.db')
curs=conn.cursor()

print ("\nLast raw Data logged on database:\n")
for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp"):
    print (str(row[0])+" ==> Temp = "+str(row[1])+"	Hum ="+str(row[2]))
