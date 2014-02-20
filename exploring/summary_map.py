#!/usr/bin/python

import json
import sys

# Read all lines from stdin
for line in sys.stdin:
   # Parse the JSON
   data = json.loads(line)

   # Emit every field
   for field in data.keys():
      print field
