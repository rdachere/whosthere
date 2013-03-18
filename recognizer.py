#! /usr/bin/env python

# Read the output of an Arduino which is constantly printing sensor output.
# See also
# http://www.arcfn.com/2009/06/arduino-sheevaplug-cool-hardware.html
# http://shallowsky.com

import sys, serial, threading
from subprocess import call
from time import time, sleep
import datetime

BASEDIR_FOR_GIT_IMAGES = "./snaps/"
MAX_TRIGGER_DISTANCE = 30   # inches
MIN_TRIGGER_DISTANCE = 0    # inches
VALID_PIC_THRESHOLD = 5     # weak attempt at mitigating "noise" (butterfly/moth/squirrel)

class Arduino(threading.Thread) :
    def run(self, interactive) :

        global BASEDIR_FOR_GIT_IMAGES, MIN_TRIGGER_DISTANCE, MAX_TRIGGER_DISTANCE

        # Port may vary, so look for it:
        baseport = "/dev/ttyACM0"
        self.ser = serial.Serial(baseport, 115200, timeout=800)
        if not self.ser :
            print "Couldn't open a serial port"
            sys.exit(1)
        print "Opened ", baseport

        self.ser.flushInput()
	valid_pic_count = 0
        while True :
            data = self.ser.readline().strip()
            if data :
                if interactive :
                    print data
		    if int(data) > MIN_TRIGGER_DISTANCE and int(data) < MAX_TRIGGER_DISTANCE:

                       print "******  DETECTED AN OBJECT AT --    ", data ,"-- INCHES ****** "

		       valid_pic_count += 1

		       if valid_pic_count == VALID_PIC_THRESHOLD:

			  #build snapshot filename with date and timestamp
			  now = datetime.datetime.now()
			  snapshot_filename = "visitor-%d:%d:%d-%d:%d:%d.jpg" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

 			  #take a photo and reset valid_pic_count
			  take_snapshot_cmd = "fswebcam "+ BASEDIR_FOR_GIT_IMAGES + snapshot_filename

			  print "\n\n************************** TAKING SNAPSHOT:  %s  ************************ \n\n" % take_snapshot_cmd
 
			  snapshot_return_code = call(take_snapshot_cmd, shell=True)
			  #print "Snapshot return code is ", snapshot_return_code
			  
			  print "\n\n************************** DOING GIT STUFF.... ***********************\n\n"

			  do_git_stuff = "git add " + BASEDIR_FOR_GIT_IMAGES + \
					  "; git commit -m \"another visitor\" " + BASEDIR_FOR_GIT_IMAGES + \
					  "; git push"

			  git_cmds_return_code = call(do_git_stuff, shell=True)

			  #print "Git stuff return code is ", git_cmds_return_code

			  sleep(3)

			  #send sms with url to the latest visitor photo

			  print "\n\n****************************  CALLING SEND_SMS COMMAND.... **********************\n\n"

			  send_sms_cmd = "python ./send_sms.py -u https://github.com/rdachere/whosthere/blob/master/snaps/" + snapshot_filename
			  sms_url_rc = call(send_sms_cmd, shell=True)

			  valid_pic_count = 0
			  
			  #sleep for a short while before checking again
			  sleep(20)

			  print "Done sleeping  - I'm awake again!!!! "
		          continue	
                else:
                    print data

# If -i, run in interactive mode
if len (sys.argv) > 1 and sys.argv[1] == '-i' :
    interactive = True
else :
    interactive = False

arduino = Arduino()
arduino.run(interactive)
