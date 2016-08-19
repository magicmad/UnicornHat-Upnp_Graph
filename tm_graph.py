#!/usr/bin/env python3

import unicornhat as unicorn
import time
import sys,subprocess
import _thread


# set max bandwidth
maxin = 750000 
maxout = 64000

colorIn =   [0,   255,   0]
colorOut =  [255,   0,   0]
colorBoth = [150,   0, 150]

# init unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(0.4)
#unicorn.rotation(180)


def getRate():
	#print ("getRate")

	global ledIn, ledOut

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
		
		# calc number of LEDs to light (0-5)
		ledIn = int( percin / 20)
		ledOut = int( percout / 20)
		#print ("IN:" + str(ledIn))


def lightColumn(x,y,r,g,b):
#	print(str(y))
	for c in range(y):
		unicorn.set_pixel(x,c,r,g,b)

def paint():
	#print ("paint!")

	# register for last 8 LED values
	rateIn = [0,0,0,0,0,0,0,0]
	rateOut = [0,0,0,0,0,0,0,0]

	offCounter = 0
	
	while 1:
		# get current rate to ledIn and LedOut values
		getRate()
		#print ("rate: " + str(ledIn) + " - " + str(ledOut))

		# TEST
		#ledIn = 3
		#ledOut = 3

		if ledIn < 0:
			# error
			#print("error")
			for x in range(8):
				for y in range(4):
					unicorn.set_pixel(x,y,255,0,0)
			unicorn.show()
		else:
			#remove oldest values
			rateIn = rateIn[:-1]
			rateOut = rateOut[:-1]

			#add new values
			rateIn = [ledIn] + rateIn
			rateOut = [ledOut] + rateOut

			# turn all off
			for x in range(8):
				for y in range(4):
					unicorn.set_pixel(x,y,0,0,0)

			# paint input
			for x in range(8):
				if rateIn[x] == rateOut[x]:
					lightColumn(x, rateIn[x], colorBoth[0], colorBoth[1], colorBoth[2])
				elif rateIn[x] > rateOut[x]:
					lightColumn(x, rateIn[x], colorIn[0], colorIn[1], colorIn[2])
					lightColumn(x, rateOut[x], 250, 0, 0)
				else:
					lightColumn(x, rateOut[x],250,0,0)
					lightColumn(x, rateIn[x], colorIn[0], colorIn[1], colorIn[2])

			if ledIn == 0 and ledOut == 0:
				offCounter += 1
			else:
				offCounter = -8

			if offCounter == 8:
				offCounter = 0
				unicorn.set_pixel(7, 0, 0, 0, 250)

			unicorn.show()

		time.sleep(0.3)


#create tread 
try:
	_thread.start_new_thread( paint, () )
	
	# keep alive
	while 1:
		pass

except:
	print ("Error: unable to start thread")

