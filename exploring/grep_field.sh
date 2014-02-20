#!/bin/bash
grep -Eo "\"$1\": [^,]+" | cut -d: -f2- | tr -d '" '
