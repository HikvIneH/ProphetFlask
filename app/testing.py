import unittest

from flask_testing import TestCase

from app import create_app, db
from app.models import User


class TestBase(TestCase):
    def create_app(self):
        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2016@localhost/dreamteam_test'
        )
        return app

    def setUp(self):
        db.create_all()
        # create test non-admin user
        employee = User(username="test_user", password="test2016")
        # save users to database
        db.session.add(User)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()