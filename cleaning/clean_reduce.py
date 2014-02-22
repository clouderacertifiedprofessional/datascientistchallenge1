#!/usr/bin/python

import json
import sys

def main():
   currentSession = None
   lastTime = None
   data = {}

   for line in sys.stdin:
      key, value = line.strip().split('\t')
      userid, timestr, sessionid = key.split(',')
      flag, payload = value.split(':')

      if sessionid != currentSession:
         currentSession = sessionid;
         kid = None

         if data:
            data['end'] = lastTime

            print json.dumps(data)

            data = {"popular": [], "recommended": [], "searched": [], "hover": [], "queued": [], 
                 "browsed": [], "recommendations": [], "recent": [], "played": {}, "rated": {}, "reviewed": {}, 
                 "actions": [], "kid": kid, "user": userid, "session": sessionid, "start": timestr}

      if flag == "C":
         data['recommendations'].extend(payload.split(","))
      elif flag == "L":
         data['actions'].append('login')
      elif flag == "P":
         data['popular'].extend(payload.split(","))
      elif flag == "R":
         data['recommended'].extend(payload.split(","))
      elif flag == "S":
         data['searched'].extend(payload.split(","))
      elif flag == "a":
         data['queued'].append(payload)
      elif flag == "c":
         data['actions'].append(payload)
         data['kid'] = False
      elif flag == "h":
         data['hover'].append(payload)
      elif flag == "i":
         data['browsed'].append(payload)
      elif flag == "l":
         data['actions'].append('logout')
      elif flag == "p":
         (marker, itemid) = payload.split(",")
         data['played'][itemid] = marker
      elif flag == "q":
         data['actions'].append('reviewedQueue')
      elif flag == "r":
         data['recent'].extend(payload.split(","))
      elif flag == "t":
         (itemid, rating) = payload.split(",")
         data['rated'][itemid] = rating
      elif flag == "v":
         data['actions'].append('verifiedPassword')
         data['kid'] = False
      elif flag == "w":
         (itemid, rating, length) = payload.split(",")
         data['reviewed'][itemid] = {}
         data['reviewed'][itemid]["rating"] = rating
         data['reviewed'][itemid]["length"] = length
      elif flag == "x":
         # If we see a parental controls event, assume this session was the opposite and start a new session
         data['kid'] = payload != "kid"
         data['end'] = lastTime

         print json.dumps(data)

         data = {"popular": [], "recommended": [], "searched": [], "hover": [], "queued": [],
                 "browsed": [], "recommendations": [], "recent": [], "played": {}, "rated": {}, "reviewed": {},
                 "actions": [], "kid": payload == "kid", "user": userid, "session": sessionid, "start": timestr}

      lastTime = timestr

   data['end'] = lastTime

   print json.dumps(data, sort_keys=True)
   
if __name__ == '__main__':
   main()
