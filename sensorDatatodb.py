import time
import sqlite3 as lite
import Adafruit_DHT

idcounter = 0
dbname = 'humidityTemp_data.db'

def getdata():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 16) 
	if humidity is not None and temperature is not None:
		humidity = round(humidity, 4)
		temperature = round(temperature, 4)
	
	return temperature, humidity
	
def logData(temperature, humidity):
	conn = lite.connect(dbname)
	curs = conn.cursor()
	curs.execute("INSERT INTO DHT_data VALUES(datetime('now'), (?), (?))", (temperature, humidity))
	conn.commit()
	conn.close()

def main():
	while True:
		temperature, humidity = getdata()
		logData(temperature, humidity)
		time.sleep(5)
		
main()
