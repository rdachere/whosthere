#!/usr/bin/env python

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

import optparse
import sys
 
# Find these values at https://twilio.com/user/account
account_sid = "AC881136e202156d7824993ec5b836aee8"
auth_token = "89e640bdf91556f21bad7f3254da87ec"
client = TwilioRestClient(account_sid, auth_token)
 
parser = optparse.OptionParser()

parser.add_option('-u', '--sms_url',
    action="store", dest="sms_url",
    help="sms url string", default="spam")

options, args = parser.parse_args()

if options.sms_url == "spam":
  print "**** HEY! You forgot the URL for the SMS: ***"
  print "**** Usage: send_sms -u <URL_string> ***"
  sys.exit()

print '\n\n ************************ SENDING SMS WITH URL: ', options.sms_url ," *************************\n\n"

body_url = "Visitor @FrontDoor: " + options.sms_url
message = client.sms.messages.create(to="+14083483184", from_="+14084588509",
                                     body=body_url)
