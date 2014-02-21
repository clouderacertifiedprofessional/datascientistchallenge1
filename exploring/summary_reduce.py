#!/usr/bin/python

import dateutil.parser
import re
import sys

"""
Figure out what type the field is and print appropriate summary stats.
"""
def print_summary():
   if is_heading:
      print "%s - %d" % (last, count)
   elif is_date:
      print "%s - min: %s, max %s, count: %d" % (last, min, max, count)
   elif is_number:
      print "%s - min: %d, max %d, average: %.2f, count: %d" % (last, min, max, float(sum)/count, count)
   elif is_value:
      print "%s - %s, count: %d" % (last, list(values), count)
   else:
      print "%s - identifier, count: %d" % (last, count)

last = None
values = set()
is_date = True
is_number = False
is_value = False
is_heading = True
min = None
max = None
sum = 0
count = 0

# Pattern to match a date time field
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})')

# Read all lines from stdin
for line in sys.stdin:
   # Split on tab. The first part is the key. The second is the value.
   parts = line.strip().split('\t')

   if parts[0] != last:
      # If there's a previous key, print its summary
      if last != None:
         print_summary()

      # Reset all the summary stats variables
      last = parts[0]
      values = set()
      is_date = True
      is_number = False
      is_identifier = False
      is_heading = True
      min = None
      max = None
      sum = 0
      count = 0

   # Increment the number of times we've seen the field
   count += 1

   # If there was a value of non-zero length, process it
   if len(parts) > 1 and len(parts[1]) > 0:
      is_heading = False

      # If we think it's a date, test if this value parses as a date
      if is_date:
         if date_pattern.match(parts[1]):
            try:
               tstamp = dateutil.parser.parse(parts[1])

               # If it does, update the summary stats.
               if min == None or tstamp < min:
                  min = tstamp

               if max == None or tstamp > max:
                  max = tstamp
            except (TypeError, ValueError):
               # If it doesn't parse, then assume it's a number
               is_date = False
               is_number = True
               min = None
               max = None
         else:
            # If it doesn't match, then assume it's a number
            is_date = False
            is_number = True
            min = None
            max = None
            
      # If we think it's a number, test it this value parses as a number
      if is_number:
         try:
            num = int(parts[1])
            sum += num

            # If so, update the summary stats
            if min == None or num < min:
               min = num

            if max == None or num > max:
               max = num
         except ValueError:
            # If not, assume it's categorical
            is_number = False
            is_value = True

      # If we think it's categorical, and this value to the category set
      if is_value:
         values.add(parts[1])

         # If there are too many categories, call it an identifier
         if len(values) > 10:
            is_value = False
            values = None

# Print the summary for the last key
print_summary()
