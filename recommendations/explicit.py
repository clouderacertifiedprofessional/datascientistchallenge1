#!/usr/bin/python

import datetime
import dateutil.parser
import json
import sys

def main():
   before = sys.argv[1] == 'before'
   cutoff = dateutil.parser.parse(sys.argv[2])
   epoch = datetime.datetime(1970,1,1,tzinfo=cutoff.tzinfo)

   # Read all lines from stdin
   for line in sys.stdin:
      data = json.loads(line)
      start = cutoff - datetime.timedelta(seconds=long(data['start']))

      if (before and start > epoch) or (not before and start <= epoch):
         for item, rating in data['rated'].iteritems():
            print "%s,%s,%s" % (data['user'], item, rating)

         for item, dict in data['reviewed'].iteritems():
            print "%s,%s,%s" % (data['user'], item, dict['rating'])

if __name__ == '__main__':
   main()
