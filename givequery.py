#!/usr/bin/env python
#-*- coding: utf-8 -*-

import urllib
import sys
import os
import cgi

### INIT VARS
if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		item = qs['item'][0]
	except:
		item = "Q1742717"
	try:
		radius = int(qs['radius'][0])
	except:
		radius = 1
	try:
		typ = qs['type'][0]
		if typ == "itemNenafoceno":
			f = "searchByItemNenafoceno.txt"
		elif typ == "itemNafoceno":
			f = "searchByItemNafoceno.txt"
	except:
		f = "searchByItemNenafoceno.txt"
else:
	item = "Q1742717"
	radius = 1
	f = "aa"

f = "../" + f

# HTML header
header = """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8" />
                <title>Titulek</title>
"""
# HTML tail
tail = """
        </body>
</html>
"""

#Load query from the file, replace 
query = open(f).read().replace('@@@ITEM@@@', item).replace('@@@RADIUS@@@', str(radius))

url = "https://query.wikidata.org/embed.html#" + urllib.quote(query)

content = '<iframe style="width:80vw; height:50vh;" frameborder="0" src="' + url + '">'

print header
print content
print tail
