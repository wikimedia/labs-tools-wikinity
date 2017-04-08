#!/usr/bin/env python
#-*- coding: utf-8 -*-

home = "/data/project/urbanecmbot/"
log = open(home + 'access.log').readlines()

num = 0
for entry in log:
	if 'map.py' in entry:
		num += 1
print """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8" />
	</head>
	<body>
		<i><p id="stat">Tento nástroj vygeneroval již """ + str(num) + """ map.</p></i>
	</body>
</html>
"""
