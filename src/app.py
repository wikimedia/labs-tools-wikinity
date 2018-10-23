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
from flask import redirect, request, jsonify, render_template, url_for, \
    make_response
from flask import Flask
import requests
from flask_jsonlocale import Locales
from flask_mwoauth import MWOAuth
from SPARQLWrapper import SPARQLWrapper, JSON
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='../static')

# Load configuration from YAML file
__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, os.environ.get(
        'FLASK_CONFIG_FILE', 'config.yaml')))))
locales = Locales(app)
_ = locales.get_message

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Layer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(6))
    definition = db.Column(db.Text)
    name = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(3))
    test = db.Column(db.Boolean)


mwoauth = MWOAuth(
    consumer_key=app.config.get('CONSUMER_KEY'),
    consumer_secret=app.config.get('CONSUMER_SECRET'),
    base_url=app.config.get('OAUTH_MWURI'),
)
app.register_blueprint(mwoauth.bp)

stats_filename = app.config.get(
    'STATS_COUNTER_FILE',
    '/tmp/wikinity-stats.txt'
)

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
            'https://' + request.headers['Host'] +
            request.headers['X-Original-URI'],
            code=301
        )

@app.before_request
def db_check_language_permissions():
    if logged():
        user = User.query.filter_by(
            username=mwoauth.get_current_user()
        ).first()
        if user is None:
            user = User(
                username=mwoauth.get_current_user(),
                language=locales.get_locale())
            db.session.add(user)
            db.session.commit()
        else:
            if user.is_active:
                locales.set_locale(user.language)
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


def make_error(errorcode):
    return make_response(jsonify({
        "errorcode": errorcode,
        "errortext": _(errorcode)
    }), 400)

def isadmin():
    if logged():
        user = User.query.filter_by(
            username=mwoauth.get_current_user(),
            is_admin=True,
            is_active=True
        )
        return user.count() == 1
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change_language', methods=['GET', 'POST'])
def change_language():
    if request.method == 'GET':
        return render_template(
            'change_language.html',
            locales=locales.get_locales(),
            permanent_locale=locales.get_permanent_locale()
        )
    else:
        if logged():
            user = User.query.filter_by(
                username=mwoauth.get_current_user()
            ).one()
            user.language = request.form.get('locale', 'en')
            db.session.add(user)
            db.session.commit()
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
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        if lat is None or lon is None or lat == '' or lon == '':
            return make_error("missing-coordinates")

        # Conversion from string to float and back is to ensure
        # the string contains correct coordinate format
        try:
            lat = str(float(lat))
            lon = str(float(lon))
        except ValueError:
            return make_error("invalid-coordinates")
    else:
        if typ == "article":
            typ = "item"
            article = request.args.get('article')
            project = request.args.get('project')

            if (
                article is None or project is None or
                article == '' or project == ''
            ):
                    return make_error("missing-article")

            r = requests.get('https://www.wikidata.org/w/api.php', params={
                "action": "wbgetentities",
                "format": "json",
                "sites": project,
                "titles": article
            })
            item = list(r.json()['entities'].keys())[0]
            if item == '-1':
                return make_error("nonexistent-article")
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

    query = "\n".join((
        open(os.path.join(__dir__, '../queries/start-%s.txt' % typ)).read(),
        get_layers_query(),
        open(os.path.join(
            __dir__, '../queries/where-%s.txt' % subtype
        )).read(),
        open(os.path.join(__dir__, '../queries/end.txt')).read()
    ))
    if typ == "coordinate":
        query = query\
            .replace('@@LAT@@', lat)\
            .replace('@@LON@@', lon)\
            .replace('@@RADIUS@@', str(radius))
    else:
        query = query\
            .replace('@@ITEM@@', item)\
            .replace('@@RADIUS@@', str(radius))

    if 'onlyquery' in request.args:
        return query

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    wd_res = sparql.query().convert()
    if 'onlywd' in request.args:
        return jsonify(wd_res)
    wikidata = {}
    layers_src = Layer.query.all()
    layers = {}
    for layer in layers_src:
        layers[layer.name] = layer.id
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
                "html_name": '<span class="legend-item" \
                    style="background-color: #%s"></span> %s' % (rgb, layer),
                "color": rgb,
                "points": []
            }
        coord = point['coord']['value']\
            .replace('Point(', '')\
            .replace(')', '')\
            .split(' ')
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

def get_layers_query():
    layers = Layer.query.all()
    res = ""
    for layer in layers:
        res += """
        OPTIONAL {
            %s
            BIND("%s" AS ?layer)
            BIND("%s" as ?rgb)
        }
        """ % (layer.definition, layer.name, layer.color)
    return res

@app.route('/admin')
def admin():
    return render_template('admin/index.html')

@app.route('/admin/users')
def admin_users():
    return render_template('admin/users.html', users=User.query.all())

@app.route('/admin/user/<path:id>', methods=['GET', 'POST'])
def admin_user(id):
    if request.method == 'POST':
        user = User.query.get(id)
        user.is_active = int(request.form.get('isactive', 0)) == 1
        user.is_admin = int(request.form.get('isadmin', 0)) == 1
        db.session.add(user)
        db.session.commit()
    return render_template('admin/user.html', user=User.query.get(id))

@app.route('/admin/layers')
def admin_layers():
    return render_template('admin/layers.html', layers=Layer.query.all())

@app.route('/admin/layer/new', methods=['GET', 'POST'])
def admin_layer_new():
    if request.method == 'GET':
        return render_template('admin/layer.html')
    else:
        layer = Layer(
            color=request.form['color'],
            definition=request.form['definition'],
            name=request.form['name']
        )
        db.session.add(layer)
        db.session.commit()
        return redirect(url_for(
            'admin_layer',
            id=Layer.query.filter_by(name=request.form['name']).one().id)
        )

@app.route('/admin/layer/<path:id>', methods=['GET', 'POST'])
def admin_layer(id):
    if request.method == 'GET':
        return render_template('admin/layer.html', layer=Layer.query.get(id))
    else:
        layer = Layer.query.get(id)
        layer.color = request.form['color']
        layer.definition = request.form['definition']
        layer.name = request.form['name']
        db.session.add(layer)
        db.session.commit()
        return render_template('admin/layer.html', layer=layer, success=True)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
