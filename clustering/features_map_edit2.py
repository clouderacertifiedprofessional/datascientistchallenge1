#!/usr/bin/env python

import sys
import json

def main():
   # Read all lines from stdin
    for line in sys.stdin:
        session = json.loads(line)
        fields = []

        fields.append(session['session'])

        fields.append('updatePassword' in session['actions'])
        fields.append('updatePaymentInfo' in session['actions'])
        fields.append('verifiedPassword' in session['actions'])
        fields.append('reviewedQueue' in session['actions'])
        fields.append(session['kid'])

#        session_duration = (long(session['end']) - long(session['start']))
#        fields.append(session_duration)

        played = set(session['played'].keys())
#        browsed = set(session['browsed'])
#        hovered = set(session['hover'])
#        queued = set(session['queued'])
        recommendations = set(session['recommendations'])
        rated = set(session['rated'].keys())
        reviewed = set(session['reviewed'].keys())
        searched = set(session['searched'])

        fields.append(len(played))
#        fields.append(len(browsed))
#        fields.append(len(hovered))
#        fields.append(len(queued))
        fields.append(len(recommendations))
        fields.append(len(rated))
        fields.append(len(reviewed))
        fields.append(len(searched))

        print ','.join(map(str, fields))

if __name__ == '__main__':
    main()

