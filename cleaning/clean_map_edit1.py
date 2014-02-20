#!/usr/bin/python

import dateutil.parser
import json
import sys
from datetime import tzinfo, timedelta, datetime

def main():
   for line in sys.stdin:
      # Correct for double quotes
      data = json.loads(line.replace('""', '"'))

      # Correct for variance in field names
      item_id = 'item_id'
      session_id = 'session_id'
      created_at = 'created_at'

      if 'sessionID' in data:
         session_id = 'sessionID'

      if 'createdAt' in data:
         created_at = 'createdAt'
      elif 'craetedAt' in data:
         created_at = 'craetedAt'

      if 'payload' in data and 'itemId' in data['payload']:
         item_id = 'itemId'

      # Prepare the key
      userid = data['user']
      sessionid = data[session_id]
      timestamp = total_seconds(dateutil.parser.parse(data[created_at]) - EPOCH)

      key = '%s,%10d,%s' % (userid, timestamp, sessionid)

      # Write out the value
      if data['type'] == "Account" and data['payload']['subAction'] == "parentalControls":
         print "%s\tx:%s" % (key, data['payload']['new'])
      elif data['type'] == "Account":
         print "%s\tc:%s" % (key, data['payload']['subAction'])
      elif data['type'] == "AddToQueue":
         print "%s\ta:%s" % (key, data['payload'][item_id])
      elif data['type'] == "Home":
         print "%s\tP:%s" % (key, ",".join(data['payload']['popular']))
         print "%s\tR:%s" % (key, ",".join(data['payload']['recommended']))
         print "%s\tr:%s" % (key, ",".join(data['payload']['recent']))
      elif data['type'] == "Hover":
         print "%s\th:%s" % (key, data['payload'][item_id])
      elif data['type'] == "ItemPage":
         print "%s\ti:%s" % (key, data['payload'][item_id])
      elif data['type'] == "Login":
         print "%s\tL:" % key
      elif data['type'] == "Logout":
         print "%s\tl:" % key
      elif data['type'] == "Play" or \
           data['type'] == "Pause" or \
           data['type'] == "Position" or \
           data['type'] == "Stop" or \
           data['type'] == "Advance" or \
           data['type'] == "Resume":
         if len(data['payload']) > 0:
            print "%s\tp:%s,%s" % (key, data['payload']['marker'], data['payload'][item_id])
      elif data['type'] == "Queue":
         print "%s\tq:" % key
      elif data['type'] == "Rate":
         print "%s\tt:%s,%s" % (key, data['payload'][item_id], data['payload']['rating'])
      elif data['type'] == "Recommendations":
         print "%s\tC:%s" % (key, ",".join(data['payload']['recs']))
      elif data['type'] == "Search":
         print "%s\tS:%s" % (key, ",".join(data['payload']['results']))
      elif data['type'] == "VerifyPassword":
         print "%s\tv:" % key
      elif data['type'] == "WriteReview":
         print "%s\tw:%s,%s,%s" % (key, data['payload'][item_id], data['payload']['rating'], data['payload']['length'])

"""
Return the number of seconds since the epoch, calculated the hard way.
"""
def total_seconds(td):
   return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

"""
A constant for 0 time difference
"""
ZERO = timedelta(0)

"""
A Timezone class for UTC
"""
class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

"""
A constant for the beginning of the epoch
"""
EPOCH = datetime(1970,1,1,tzinfo=UTC())

if __name__ == '__main__':
   main()
