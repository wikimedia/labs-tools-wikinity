from unittest import TestCase
import re

from src.app import app, db
from sqlalchemy_utils.functions import database_exists, create_database

def remove_whitespace(s):
    return re.sub(r"\s", "", s)

class BasicTests(TestCase):
    def setUp(self):
        self.app = app.test_client()
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        with app.app_context():
            db.create_all()

    def test_map(self):
        types = {
            "coordinate": [
                "lat=50.088611&lon=14.421389"
            ],
            "article": [
                "article=Praha&project=cswiki"
            ],
            "item": [
                "item=Q142"
            ]
        }
        subtypes = ["unphotographed", "photographed", "all"]
        for type in types:
            for subtype in subtypes:
                for data_query in types[type]:
                    urls = [
                        '/map?type=%s&radius=5&subtype=%s&%s&onlyquery'
                        % (type, subtype, data_query),
                        '/map?type=%s&radius=5&subtype=%s&%s&onlywd'
                        % (type, subtype, data_query),
                        '/map?type=%s&radius=5&subtype=%s&%s'
                        % (type, subtype, data_query),
                    ]
                    for url in urls:
                        response = self.app.get(url)
                        # TODO: Verify that actual returned content
                        # matches expected data
                        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
