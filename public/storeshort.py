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

if os.environ['REQUEST_METHOD'] != 'POST':
	print 'Use POST please'
	sys.exit()

form = cgi.FieldStorage()
url = form.getvalue('url')

if not url.startswith('https://tools.wmflabs.org/wikinity'):
	print 'Wrong URL'
	print "We aren't a shortener!"
	sys.exit()

cur = conn.cursor()
with cur:
	sql = 'select id from shortener where url="' + url + '"'
	cur.execute(sql)
	data = cur.fetchall()

if len(data) != 0:
	print data[0][0]
	sys.exit()

cur = conn.cursor()
with cur:
	sql = 'insert into shortener(url) values ("' + url + '");'
	cur.execute(sql)

cur = conn.cursor()
with cur:
	sql = 'select id from shortener where url="' + url + '"'
	cur.execute(sql)
	data = cur.fetchall()

print data[0][0]
