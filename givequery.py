#!/usr/bin/env python
#-*- coding: utf-8 -*-

import urllib
import sys
import os
import cgi

if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		typ = qs['type'][0]
	except:
		typ = "item"
	if typ == "coor":
		try:
			lat = qs['lat'][0]
			lon = qs['lon'][0]
		except:
			lat = "15.7802056"
			lon = "50.0385383"
		try:
			subtype = qs['subtype'][0]
		except:
			subtype = "nenafoceno"
		try:
			radius = int(qs['radius'][0])
		except:
			radius = 1
		if subtype == "nafoceno":
			f = "searchByCoorNafoceno.txt"
		elif subtype == "all":
			f = "searchByCoorAll.txt"
		else:
			f = "searchByCoorNenafoceno.txt"
	else:
		try:
			item = qs['item'][0]
		except:
			item = "Q1742717"
		try:
			radius = int(qs['radius'][0])
		except:
			radius = 1
		try:
			subtype = qs['subtype'][0]
			if subtype == "nafoceno":
				f = "searchByItemNafoceno.txt"
			elif subtype == "all":
				f = "searchByItemAll.txt"
			else:
				f = "searchByItemNenafoceno.txt"
		except:
			f = "searchByItemNenafoceno.txt"
else:
	item = "Q1742717"
	radius = 1
	f = "searchByItemNenafoceno.txt"
	typ = "item"
	subtype = "nenafoceno"

f = "../queries/" + f
header = """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8" />
                <title>Titulek</title>
"""
tail = """
        </body>
</html>
"""

if typ == "coor":
	query = open(f).read().replace('@@@LAT@@@', lat).replace('@@@LON@@@', lon).replace('@@@RADIUS@@@', str(radius))
else:
	#Create query for item type
	query = open(f).read().replace('@@@ITEM@@@', item).replace('@@@RADIUS@@@', str(radius))

# Create URL
url = "https://query.wikidata.org/embed.html#" + urllib.quote(query)

#Create content and print it
content = '<iframe style="width:80vw; height:50vh;" frameborder="0" src="' + url + '">'
print header
print content
print tail
