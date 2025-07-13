from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from website import create_app, db
from website.models import User, Contact


@pytest.fixture
def app():
    app = create_app(testing=True)

    with app.app_context():
        db.create_all()

        user = User(name="Test User", email="test@example.com", password="test")
        db.session.add(user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    class AuthActions:
        def login(self):
            client.post('/login', data={
                'name': "Test User", 
                'email': "test@example.com", 
                'password': "test"
            } ,follow_redirects=True)

        def logout(self):
            return client.get('/logout', follow_redirects=True)   
         
    return AuthActions()        


@pytest.fixture
def create_contact(app):
    def _create_contact(name):
        contact =  Contact(
            name=name, 
            date=datetime.strptime('2000-10-10', "%Y-%m-%d").date(), 
            user_id=1)
        db.session.add(contact)
        db.session.commit()
        return contact
    return _create_contact  


@pytest.fixture
def runner(app):
    return app.test_cli_runner()




