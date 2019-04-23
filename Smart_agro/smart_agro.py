from flask import Flask, render_template, redirect, session, url_for, flash, request, logging, Response
import sqlite3 as lite
import time
import os
import RPi.GPIO as GPIO
import tkinter

app = Flask(__name__)

def getData():
	conn = lite.connect('../humidityTemp_data.db')
	curs = conn.cursor()
	
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp"):
		time = str(row[0])
		temperature = row[1]
		humidity = row[2]
	conn.close()
	return time, temperature, humidity

def adcPi():
	#!/usr/bin/python

	#Analog Input with ADC0832 chip

	GPIO.setmode(GPIO.BCM)

	#SPI Port on the ADC 
	PIN_CLK = 23
	PIN_DO = 27
	PIN_DI = 22
	PIN_CS = 18

	#Set up the SPI interface pins
	GPIO.setup(PIN_DI, GPIO.OUT)
	GPIO.setup(PIN_DO, GPIO.IN)
	GPIO.setup(PIN_CLK, GPIO.OUT)
	GPIO.setup(PIN_CS, GPIO.OUT)

	#Read SPI data from ADC8032
	def getADC(channel):
		#1. CS LOW
		GPIO.output(PIN_CS, True)   #cLear Last transmission
		GPIO.output(PIN_CS, False)  #bring CS low

		#2. Start clock
		GPIO.output(PIN_CLK, False)

		#3. Input MUX address
		for i in [1,1,channel]: #start bit + mux assignment
			if(i == 1):
				GPIO.output(PIN_DI, True)

			else:
				GPIO.output(PIN_DI, False)

			GPIO.output(PIN_CLK, True)
			GPIO.output(PIN_CLK, False)

		#4. read ADC bits
		ad = 0
		for i in range(8):
			GPIO.output(PIN_CLK, True)
			GPIO.output(PIN_CLK, False)
			ad <<= 1 #shifr bit
			if(GPIO.input(PIN_DO)):
				ad |= 0x1 #set first bit

		#5. reset
		GPIO.output(PIN_CS, True)

		return ad

	if __name__ == "__main__":
		while True:
			print("ADC[0]: {}\t ADC[1]: {}".format(getADC(0), getADC(1)))
			time.sleep(1)
			return getADC(1)

		

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html', title="ABOUT")

@app.route('/hello')
def hello():
	
	value = adcPi()

	time, temperature, humidity = getData()
	templateData = {
		'time':time,
		'temperature':temperature,
		'humidity':humidity,
		'value': value
	}
	return render_template('hello.html', title="DATA", **templateData)

@app.route('/pumpon')
def pumpon():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26, GPIO.OUT)

	GPIO.output(26, True)
	return render_template('pumpon.html', title="PUMPON")

@app.route('/pumpoff')
def pumpoff():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26, GPIO.OUT)

	GPIO.output(26, False)

	GPIO.cleanup()
	return redirect(url_for('index'))

@app.route('/login')
def login():
	return render_template('login.html', title="LOGIN")
	
if __name__ == '__main__':
	app.secret_key='12345secret'
	app.run(debug=True, port=3330, host='0.0.0.0')


