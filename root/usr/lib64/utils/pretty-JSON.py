#!/usr/bin/env python
import json

with open('data.json', 'r') as handle:
    parsed = json.load(handle)

print json.dumps(parsed, indent = 4, sort_keys = True)
