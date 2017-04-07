#!/bin/bash

./visitors -A -o html --grep 'map.py' ~/access.log > public/stats.html
