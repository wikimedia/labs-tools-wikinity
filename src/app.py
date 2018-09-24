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

import os
import yaml
from flask import redirect, request, jsonify, render_template, url_for
from flask import Flask
import requests
import pymysql
from flask_jsonlocale import Locales
from flask_mwoauth import MWOAuth
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

# Load configuration from YAML file
__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))
locales = Locales(app)

mwoauth = MWOAuth(
    consumer_key=app.config.get('CONSUMER_KEY'),
    consumer_secret=app.config.get('CONSUMER_SECRET'),
    base_url=app.config.get('OAUTH_MWURI'),
)
app.register_blueprint(mwoauth.bp)

stats_filename = app.config.get('STATS_COUNTER_FILE', '/tmp/wikinity-stats.txt')

QUERY_TYPES = [
    "coordinate",
    "item",
    "photographed",
    "unphotographed",
    "all",
    "end",
]

def logged():
    return mwoauth.get_current_user() is not None

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
            cur.execute('SELECT id, is_active, language FROM users WHERE username=%s', mwoauth.get_current_user())
            data = cur.fetchall()
        if len(data) == 0:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO users(username, language) VALUES (%s, %s)', (mwoauth.get_current_user(), locales.get_locale()))
                conn.commit()
        else:
            if data[0][1] == 1:
                locales.set_locale(data[0][2])
            else:
                return render_template('permission_denied.html')

@app.before_request
def check_admin_permissions():
    if '/admin' in request.url and not isadmin():
        return render_template('permission_denied.html')

@app.context_processor
def inject_base_variables():
    return {
        "logged": logged(),
        "username": mwoauth.get_current_user(),
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

def isadmin():
    if logged():
        conn = connect()
        with conn.cursor() as cur:
            cur.execute('SELECT username FROM users WHERE is_active=1 AND is_admin=1 AND username=%s', mwoauth.get_current_user())
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
                cur.execute('UPDATE users SET language=%s WHERE username=%s', (request.form.get('locale', 'en'), mwoauth.get_current_user()))
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
        stats_num = str(int(open(stats_filename).read()) + 1)
        open(stats_filename, 'w').write(stats_num)
    except FileNotFoundError as e:
        open(stats_filename, 'w').write('1')

    typ = request.args.get('type', 'item')
    subtype = request.args.get('subtype', 'unphotographed')
    radius = int(request.args.get('radius') or 5)

    if typ == "coordinate":
        lat = request.args.get('lat') or '50.0385383'
        lon = request.args.get('lon') or '15.7802056'
    else:
        if typ == "article":
            typ = "item"
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
        r = requests.get('https://www.wikidata.org/w/api.php', params={
            "action": "wbgetclaims",
            "format": "json",
            "entity": item
        })
        data = r.json()
        coor = data["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]
        lat = coor["latitude"]
        lon = coor["longitude"]

    query = "\n".join((open('../queries/start-%s.txt' % typ).read(), get_layers_query(), open('../queries/where-%s.txt' % subtype).read(), open('../queries/end.txt').read()))
    if typ == "coor":
        query = query.replace('@@LAT@@', lat).replace('@@LON@@', lon).replace('@@RADIUS@@', str(radius))
    else:
        query = query.replace('@@ITEM@@', item).replace('@@RADIUS@@', str(radius))

    if 'onlyquery' in request.args:
        return query

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    wd_res = sparql.query().convert()
    if 'onlywd' in request.args:
        return jsonify(wd_res)
    wikidata = {}
    layers_src = get_layers()
    layers = {}
    for layer in layers_src:
        layers[layer[3]] = layer[0]
    for point in wd_res["results"]["bindings"]:
        try:
            layer = point['layer']['value']
            rgb = point['rgb']['value']
        except KeyError:
            layer = "ostatní"
            rgb = "fff"
        id = layers.get(layer, -1)
        if id not in wikidata:
            wikidata[id] = {
                "name": layer,
                "html_name": '<span class="legend-item" style="background-color: #%s"></span> %s' % (rgb, layer),
                "color": rgb,
                "points": []
            }
        coord = point['coord']['value'].replace('Point(', '').replace(')', '').split(' ')
        wikidata[id]['points'].append({
            "lat": coord[1],
            "lon": coord[0],
            "url": point['item']['value'],
            "name": point['itemLabel']['value'],
        })
    res = {
        "lat": lat,
        "lon": lon,
        "wikidata": wikidata
    }

    return jsonify(res)

def get_layers():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM layers')
        return cur.fetchall()

def get_layer(id):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM layers WHERE id=%s', id)
        return cur.fetchall()[0]

def get_layers_query():
    layers = get_layers()
    res = ""
    for layer in layers:
        res += """
        OPTIONAL {
            %s
            BIND("%s" AS ?layer)
            BIND("%s" as ?rgb)
        }
        """ % (layer[2], layer[3], layer[1])
    return res

@app.route('/admin')
def admin():
    return render_template('admin/index.html')

@app.route('/admin/users')
def admin_users():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<path:id>', methods=['GET', 'POST'])
def admin_user(id):
    conn = connect()
    if request.method == 'POST':
        with conn.cursor() as cur:
            cur.execute('UPDATE users SET is_active=%s, is_admin=%s WHERE id=%s', (int(request.form.get('isactive', 0)), int(request.form.get('isadmin', 0)), id))
        conn.commit()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE id=%s', id)
        user = cur.fetchall()[0]
    return render_template('admin/user.html', user=user)

@app.route('/admin/layers')
def admin_layers():
    return render_template('admin/layers.html', layers=get_layers())

@app.route('/admin/layer/new', methods=['GET', 'POST'])
def admin_layer_new():
    if request.method == 'GET':
        return render_template('admin/layer.html')
    else:
        conn = connect()
        with conn.cursor() as cur:
            cur.execute('INSERT INTO layers(color, definition, name) VALUES(%s, %s, %s)', (request.form['color'], request.form['definition'], request.form['name']))
        conn.commit()
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM layers ORDER BY id DESC')
        return redirect(url_for('admin_layer', id=cur.fetchall()[0][0]))

@app.route('/admin/layer/<path:id>', methods=['GET', 'POST'])
def admin_layer(id):
    if request.method == 'GET':
        return render_template('admin/layer.html', layer=get_layer(id))
    else:
        conn = connect()
        with conn.cursor() as cur:
            cur.execute('UPDATE layers SET color=%s, definition=%s, name=%s WHERE id=%s', (request.form['color'], request.form['definition'], request.form['name'], id))
        conn.commit()
        return render_template('admin/layer.html', layer=get_layer(id), success=True)


if __name__ == "__main__":
	app.run(debug=True, threaded=True)
