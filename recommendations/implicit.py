#!/usr/bin/python

import json
import sys

def main():
   # Read all lines from stdin
   for line in sys.stdin:
      data = json.loads(line)

      for item in data['rated'].keys() + data['reviewed'].keys() + data['played'].keys() + data['browsed'] + data['queued']:
         print "%s,%s" % (data['user'], item)

if __name__ == '__main__':
   main()
