#!/usr/bin/env python
#-*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
import sys
import os
import cgi

if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		email = qs['email'][0]
		title = qs['title'][0]
		body = qs['body'][0]
	except:
		sys.exit()
else:
	sys.exit()

sender = email
recipient = "bugs@webappky.cz"

mail = "!projects #wikinity\n\n" + body
msg = MIMEText(mail)
msg['Subject'] = title
msg['From'] = sender
msg['To'] = recipient
s = smtplib.SMTP('mail.tools.wmflabs.org')
s.ehlo()
s.sendmail(sender, recipient, msg.as_string())
s.quit()
