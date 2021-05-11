import pytest
from django.contrib.auth.models import User
from links.models import link, collection


@pytest.fixture()
def create_test_user():
    test_user = User.objects.create_user('test_user')
    return test_user


@pytest.fixture()
def create_test_link():
    test_user = User.objects.create_user('test_user2')
    test_link = link.objects.create(hyperlink='https://twitter.com', website_name='Twitter', user=test_user)
    return test_link


@pytest.fixture()
def create_test_collection():
    test_user = User.objects.create_user('test_user3')
    link.objects.create(hyperlink='https://twitter.com', website_name='Twitter', user=test_user)
    get_link = link.objects.all()
    test_collection = collection.objects.create(name='Test collection1', user=test_user)
    test_collection.links.set(get_link)
    return test_collection
