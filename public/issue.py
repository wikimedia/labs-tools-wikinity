#!/usr/bin/env python
#-*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
import sys
import os
import cgi
import cgitb

if os.environ['REQUEST_METHOD'] != 'POST':
	print 'Use POST please'
	sys.exit()

form = cgi.FieldStorage()
email = form.getvalue('email')
title = form.getvalue('title')
body = form.getvalue('body')

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

print "Mail sent"
