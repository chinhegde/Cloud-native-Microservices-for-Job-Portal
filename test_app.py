import pytest
from app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_search_page(client):
    response = client.get('/search')
    assert response.status_code == 200
    assert b'Keyword' in response.data

def test_user_profile_page(client):
    response = client.get('/user-profile')
    assert response.status_code == 200
    assert b'User Profile' in response.data

def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact' in response.data

def test_job_details_existing_job(client):
    response = client.get('/jobs/1')
    assert response.status_code == 200
    assert b'Apply Now' in response.data

def test_apply_existing_job(client):
    response = client.get('/apply/1')
    assert response.status_code == 200
    assert b'Job Application Form' in response.data

def test_post_job_page(client):
    response = client.get('/post-job')
    assert response.status_code == 200
    assert b'Post a Job' in response.data
