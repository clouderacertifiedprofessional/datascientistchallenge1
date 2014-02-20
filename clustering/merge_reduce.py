#!/usr/bin/python

import json
import sys

def main():
   last = None
   
   # Read all the lines from stdin
   for line in sys.stdin:
      id, str = line.strip().split('\t', 1)
   
      if id != last:
         if last != None:
            print json.dumps(data)
         
         last = id
         data = None
         
      data = merge(data, json.loads(str))
      
   print json.dumps(data)

"""
Merge the contents of new into data being mindful of types
"""      
def merge(data, new):
   if data:
      for key in new:
         if type(new[key]) == dict:
            data[key].update(new[key])
         elif type(new[key]) == list:
            data[key].extend(new[key])
         elif type(new[key]) == bool:
            data[key] |= new[key]
         elif data[key] != new[key] and key not in ['start', 'end', 'kid']:
            sys.stderr.write("Mismatch for %s on %s: %s != %s\n" % (data['session'], key, str(data[key]), str(new[key])))
   else:
      data = dict(new)
      
   return data
   
if __name__ == '__main__':
   main()
