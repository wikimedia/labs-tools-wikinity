#!/usr/bin/env python
#-*- coding: utf-8 -*-

home = "/data/project/wikinity/"
log = open(home + 'access.log').readlines()

num = 0
for entry in log:
	if 'map.py' in entry:
		num += 1

print str(num)
