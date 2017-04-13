#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import cgi
import requests
import json

if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		title = qs['title'][0]
		body = qs['body'][0]
	except:
		sys.exit()
else:
	sys.exit()

data = {}
data['title'] = title
data['body'] = body

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

owner = "urbanecm"
repo = "test"
url = 'https://api.github.com/repos/' + owner + '/' + repo + '/issues'

username = "urbanecm"
token = open('../token.txt').read()

r = requests.post(url, data=json.dumps(data), headers=headers, auth=(username, token))
