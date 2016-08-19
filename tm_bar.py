#!/usr/bin/env python3

import unicornhat as unicorn
import time
import sys,subprocess
import _thread

# set max bandwidth
maxin = 750000 
maxout = 64000


# init unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.2)

# target number of active LEDs
ledIn = 0
ledOut = 0


def getRate():
	#print ("getRate")

	global ledIn, ledOut

	while 1:
			error = False
			rate = ""
			
			# get xml from router
			try:
				rate = str(subprocess.check_output(["/home/pi/upnp/connection_rate.sh"]))
			except subprocess.CalledProcessError:
				error = True
			if rate == "":
				error = True
			else:
				sendrate = rate.split('NewByteSendRate', maxsplit=3)
				receiverate = rate.split('NewByteReceiveRate', maxsplit=3)
			
				if len(sendrate) != 3:
					error = True
				if len(receiverate) != 3:
					error = True
			if error:
				ledIn = -1
				ledOut = -1
			else:
				sendrate = sendrate[1][1:-2]
				receiverate = receiverate[1][1:-2]
				
				percin = 0
				percout = 0
				
				# calc percentage of max bandwidth used
				if receiverate != 0:
					percin = float(receiverate) / maxin * 100
				if sendrate != 0:
					percout = float(sendrate) / maxout * 100
				
				# calc number of LEDs to light
				ledIn = int( percin / 11.11)
				ledOut = int( percout / 11.11)

			#print ("IN:" + str(ledIn))
			#time.sleep(0.1)

def paint():
	#print ("paint!")

	# number of active LEDs (0-8)
	curIn = 0
	curOut = 0
	
	while 1:
		#print ("IN2:" + str(ledIn))

		curInPre = curIn
		curOutPre = curOut

		if ledIn < 0:
			for x in range(8):
				for y in range(4):
					unicorn.set_pixel(x,y,255,0,0)
			unicorn.show()
		else:
			if curIn < ledIn:
				curIn = curIn + 1
			if curIn > ledIn:
				curIn = curIn - 1
			if curOut < ledOut:
				curOut = curOut + 1
			if curOut > ledOut:
				curOut = curOut - 1

			#print (str(curIn))
			#skip painting if nothing changed
			if curOutPre == curOut and curInPre == curIn:
				continue

			# turn all off
			for x in range(8):
				for y in range(4):
					unicorn.set_pixel(x,y,0,0,0)

			# paint input
			for x in range(curIn):
				unicorn.set_pixel(x,0,0,250,0)
				unicorn.set_pixel(x,1,0,250,0)
			
			# paint output
			for x in range(curOut):
				unicorn.set_pixel(x,2,250,0,0)
				unicorn.set_pixel(x,3,250,0,0)
			
			unicorn.show()

		time.sleep(0.07)

#create unicorn tread 
#create upnp query thread
try:
	_thread.start_new_thread( getRate, () )
	_thread.start_new_thread( paint, () )
	
	# keep alive
	while 1:
		pass

except:
	print ("Error: unable to start thread")

