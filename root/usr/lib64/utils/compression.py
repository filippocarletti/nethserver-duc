#!/usr/bin/env python
import json

with open('pretty.json', 'r') as handle:
    parsed = json.load(handle)

minJSON = json.dumps(parsed, indent = 0, sort_keys = True)

wf = open("pretty.json","w")
for line in minJSON:
    newline = line.rstrip('\r\n')
    wf.write(newline)
