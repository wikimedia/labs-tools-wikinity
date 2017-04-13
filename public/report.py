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

response = """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Nahlásit problém - Wikinity</title>
                <!-- font awesome -->
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
                <!-- Latest compiled and minified CSS -->
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
                <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
                <!-- Latest compiled and minified JavaScript -->
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
        </head>
        <body>
		<!-- navbar -->
                <nav class="navbar navbar-inverse bg-faded" style="background-color:#337ab7;border-color: 2e6da4">
                <a class="navbar-brand" href="index.php" style="color: #fff"> 
                 Wikinity
                </a>
                <a class="navbar-brand" href="https://github.com/urbanecm/wikinity/" style="color: #fff;float: right">
                <i class="fa fa-github fa-lg" aria-hidden="true"></i> GitHub - zdrojový kód
                </a>
                </nav>
		<!-- Content -->
		<div class="container">
			<div class="row">
				<p>Děkujeme za nahlášení problému! Brzy se jím budeme zabývat. Nyní se můžete <a href="index.php">vrátit zpět</a> k nástroji. </p>
			</div>
		</div>
        </body>
</html>
"""
print response
