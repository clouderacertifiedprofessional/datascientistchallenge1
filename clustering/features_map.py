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
    
        played = set(session['played'].keys()) 

        fields.append(len(played))

        print ','.join(map(str, fields))

if __name__ == '__main__':
    main()
