#!/usr/bin/python

import json
import sys

# Read all lines from stdin
for line in sys.stdin:
   try:
      # Parse the JSON
      data = json.loads(line)

      # Emit every field
      for field in data.keys():
         print field
   except ValueError:
      # Log the error so we can see it
      sys.stderr.write("%s\n" % line)
      exit(1)
