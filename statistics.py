#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

CMD = "./visitors -A -o html --grep 'map.py' ~/access.log"
os.system(CMD)
