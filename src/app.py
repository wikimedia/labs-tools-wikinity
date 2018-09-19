# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import flask
import os
import yaml
import simplejson as json
from flask import redirect, request, jsonify, make_response, render_template, session, url_for
from flask import Flask
import requests
import urllib.parse
import toolforge
import pymysql
from flask_jsonlocale import Locales

app = Flask(__name__)

# Load configuration from YAML file
__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))
locales = Locales(app)

stats_filename = app.config.get('STATS_COUNTER_FILE', '/tmp/wikinity-stats.txt')

@app.before_request
def force_https():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return redirect(
            'https://' + request.headers['Host'] + request.headers['X-Original-URI'],
            code=301
        )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change_language', methods=['GET', 'POST'])
def change_language():
    if request.method == 'GET':
        return render_template('change_language.html', locales=locales.get_locales(), permanent_locale=locales.get_permanent_locale())
    else:
        locales.set_locale(request.form.get('locale'))
        return redirect(url_for('index'))

@app.route('/stats')
def stats():
    if os.path.isfile(stats_filename):
        return open(stats_filename).read()
    return '0'

@app.route('/map')
def map():
    try:
        stats_num = str(int(open(stats_filename).read())+1)
        open(stats_filename, 'w').write(stats_num)
    except:
        open(stats_filename, 'w').write('1')

    typ = request.args.get('type', 'item')
    subtype = request.args.get('subtype', 'nenafoceno')
    radius = int(request.args.get('radius') or 5)

    if typ == "coor":
        lat = request.args.get('lat') or '50.0385383'
        lon = request.args.get('lon') or '15.7802056'
        filetype = "Coor"
    else:
        if typ == "article":
            article = request.args.get('article') or 'Praha'
            project = request.args.get('project') or 'cswiki'

            r = requests.get('https://www.wikidata.org/w/api.php', params={
                "action": "wbgetentities",
                "format": "json",
                "sites": project,
                "titles": article
            })
            item = list(r.json()['entities'].keys())[0]
            if item == '-1':
                item = 'Q1085'
        else:
            item = request.args.get('item') or 'Q1085'
        
        filetype = "Item"
    if subtype == "nafoceno":
        f = "searchBy%sNafoceno.txt" % filetype
    elif subtype == "all":
        f = "searchBy%sAll.txt" % filetype
    else: # Process in nenafoceno mode
        f = "searchBy%sNenafoceno.txt" % filetype
    
    f = os.path.join('..', 'queries', f)

    if typ == "coor":
        query = open(f).read().replace('@@@LAT@@@', lat).replace('@@@LON@@@', lon).replace('@@@RADIUS@@@', str(radius))
    else:
        r = requests.get('https://wikidata.org/entity/%s.json' % item)
        data = r.json()
        if 'P625' in data['entities'][item]['claims']:
            query = open(f).read().replace('@@@ITEM@@@', item).replace('@@@RADIUS@@@', str(radius))
        else:
            return "<h1>%s</h1>" % locales.getmessage('no-coordinates')
    
    return '<iframe id="map" style="width:90vw; height:90vh;" frameborder="0" src="https://query.wikidata.org/embed.html#' + urllib.parse.quote(query) + '">'

if __name__ == "__main__":
	app.run(debug=True, threaded=True)
