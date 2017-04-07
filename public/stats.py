#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
home = os.environ['HOME'] + '/'
log = open(home + 'access.log').readlines()

num = 0
for entry in log:
	if 'map.py' in entry:
		num += 1

print "<p>Tento nástroj vygeneroval již " + str(num) + " map.</p>"
