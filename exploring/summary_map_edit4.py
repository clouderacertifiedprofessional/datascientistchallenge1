#!/usr/bin/python

import json
import sys

# Read all lines from stdin
for line in sys.stdin:
   try:
      # Parse the JSON after fixing the quotes
      data = json.loads(line.replace('""', '"'))

      for field in data.keys():
         if field == 'type':
            # Just emit the type field when we see it
            print "%s" % (data[field])
         else:
            # Normalize the file name
            real = field

            if real == 'user_agent':
               real = 'userAgent'
            elif real == 'session_id':
               real = 'sessionID'
            elif real == 'created_at' or real == 'craetedAt':
               real = 'createdAt'

            # Emit all subfields, if there are any
            if type(data[field]) is dict:
               print "%s:%s" % (data['type'], real)

               # Normalize and print the subfields
               for subfield in data[field]:
                  subreal = subfield

                  if subreal == 'item_id':
                     subreal = 'itemId'
                  
                  print "%s:%s:%s\t%s" % (data['type'], real, subreal, data[field][subfield])
            else:
               # Emit the normalized field
               print "%s:%s\t%s" % (data['type'], real, data[field])

   except ValueError:
      # Log the error so we can see it
      sys.stderr.write("%s\n" % line)
      exit(1)
