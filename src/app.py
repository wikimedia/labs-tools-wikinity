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
import mwoauth
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

@app.before_request
def db_check_language_permissions():
    if logged():
        conn = connect()
        with conn.cursor() as cur:
            cur.execute('SELECT id, is_active, language FROM users WHERE username=%s', getusername())
            data = cur.fetchall()
        if len(data) == 0:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO users(username, language) VALUES (%s, %s)', (getusername(), locales.get_locale()))
                conn.commit()
        else:
            if data[0][1] == 1:
                locales.set_locale(data[0][2])
            else:
                return render_template('permission_denied.html')

@app.context_processor
def inject_base_variables():
    return {
        "logged": logged(),
        "username": getusername(),
        "admin": isadmin()
    }

def connect():
    if app.config.get('DB_CONF'):
        return pymysql.connect(
            database=app.config.get('DB_NAME'),
            host=app.config.get('DB_HOST'),
            read_default_file=app.config.get('DB_CONF')
        )
    else:
        return pymysql.connect(
            database=app.config.get('DB_NAME'),
            host=app.config.get('DB_HOST'),
            user=app.config.get('DB_USER'),
            password=app.config.get('DB_PASS')
        )

def logged():
	return flask.session.get('username') != None

def getusername():
    return flask.session.get('username')

def isadmin():
    if logged():
        conn = connect()
        with conn.cursor() as cur:
            cur.execute('SELECT username FROM users WHERE is_active=1 AND is_admin=1 AND username=%s', getusername())
            return len(cur.fetchall()) == 1
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change_language', methods=['GET', 'POST'])
def change_language():
    if request.method == 'GET':
        return render_template('change_language.html', locales=locales.get_locales(), permanent_locale=locales.get_permanent_locale())
    else:
        if logged():
            conn = connect()
            with conn.cursor() as cur:
                cur.execute('UPDATE users SET language=%s WHERE username=%s', (request.form.get('locale', 'en'), getusername()))
            conn.commit()
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

def get_queries():
    conn = connect()
    queries = {}
    types = [
        "layers",
        "coordinate",
        "item",
        "photographed",
        "unphotographed",
        "end",
    ]
    queries = {}
    for typ in types:
        with conn.cursor() as cur:
            cur.execute('SELECT query FROM query WHERE type=%s ORDER BY timestamp DESC LIMIT 1', typ)
            data = cur.fetchall()
            if len(data) == 1:
                queries[typ] = data[0][0]
            else:
                queries[typ] = ""
    return queries

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if logged():
        if not isadmin():
            return render_template('permission_denied.html')
        if request.method == 'GET':
            return render_template('admin.html', queries=get_queries())
        else:
            conn = connect()
            queries = get_queries()
            for typ in request.form:
                if typ.startswith('query-') and queries[typ.replace('query-', '')] != request.form.get(typ):
                    with conn.cursor() as cur:
                        cur.execute('INSERT INTO query(query, type, username) VALUES(%s, %s, %s)', (request.form.get(typ), typ.replace('query-', ''), getusername()))
            conn.commit()
            return render_template('admin.html', queries=get_queries())
    else:
        return redirect(url_for("login"))

@app.route('/login')
def login():
	"""Initiate an OAuth login.
	Call the MediaWiki server to get request secrets and then redirect the
	user to the MediaWiki server to sign the request.
	"""
	consumer_token = mwoauth.ConsumerToken(
		app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
	try:
		redirect, request_token = mwoauth.initiate(
		app.config['OAUTH_MWURI'], consumer_token)
	except Exception:
		app.logger.exception('mwoauth.initiate failed')
		return flask.redirect(flask.url_for('index'))
	else:
		flask.session['request_token'] = dict(zip(
		request_token._fields, request_token))
		return flask.redirect(redirect)

@app.route('/oauth-callback')
def oauth_callback():
	"""OAuth handshake callback."""
	if 'request_token' not in flask.session:
		flask.flash(u'OAuth callback failed. Are cookies disabled?')
		return flask.redirect(flask.url_for('index'))
	consumer_token = mwoauth.ConsumerToken(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])

	try:
		access_token = mwoauth.complete(
		app.config['OAUTH_MWURI'],
		consumer_token,
		mwoauth.RequestToken(**flask.session['request_token']),
		flask.request.query_string)
		identity = mwoauth.identify(app.config['OAUTH_MWURI'], consumer_token, access_token)
	except Exception:
		app.logger.exception('OAuth authentication failed')
	else:
		flask.session['request_token_secret'] = dict(zip(access_token._fields, access_token))['secret']
		flask.session['request_token_key'] = dict(zip(access_token._fields, access_token))['key']
		flask.session['username'] = identity['username']

	return flask.redirect(flask.url_for('index'))


@app.route('/logout')
def logout():
	"""Log the user out by clearing their session."""
	flask.session.clear()
	return flask.redirect(flask.url_for('index'))


if __name__ == "__main__":
	app.run(debug=True, threaded=True)
