#!/usr/bin/python

import re
import sys

def main():
   p = re.compile('.*"session": "([^"]+)".*')
   
   # Read all the lines from stdin
   for line in sys.stdin:
      m = p.match(line)
      
      if m:
         print "%s\t%s" % (m.group(1), line.strip())
      else:
         sys.strerr.write("Failed to find ID in line: %s" % line)
   
if __name__ == '__main__':
   main()
