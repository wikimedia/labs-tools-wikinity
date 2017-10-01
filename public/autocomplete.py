#!/usr/bin/env python
#-*- coding: utf-8 -*-

import yaml
config = yaml.load(open('config.yaml'))
from wmflabs import db
import sys
import os
import cgi
import json

if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		start = qs['start'][0]
		thing = qs['thing'][0]
		project = qs['project'][0]
	except:
		print 'Bad request'
		sys.exit()
else:
	print 'Add something to query string'
	sys.exit()

conn = db.connect(project)

if thing == 'article':
	cur = conn.cursor()
	with cur:
		sql = 'select page_title from page where page_namespace=0 and page_title like "' + start + '%" order by page_title limit 10'
		cur.execute(sql)
		data = cur.fetchall()
	pages = []
	for row in data:
		pages.append(row[0])
	print json.dumps(pages)
else:
	print 'Bad request'
