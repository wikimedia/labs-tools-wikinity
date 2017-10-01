#!/usr/bin/env python
#-*- coding: utf-8 -*-

import yaml
config = yaml.load(open('config.yaml'))
from wmflabs import db
conn = db.connect(config['DB_NAME'])
import sys
import os
import cgi
import cgitb

if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	id = qs.keys()[0]
else:
	print 'Add something to query string'
	sys.exit()

print id
