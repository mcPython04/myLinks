import pytest
from django.contrib.auth.models import User
from links.models import link


@pytest.fixture()
def create_test_user():
    test_user = User.objects.create_user('test_user')
    return test_user


@pytest.fixture()
def create_test_link():
    test_user = User.objects.create_user('test_user2')
    test_link = link.objects.create(hyperlink='https://twitter.com', website_name='Twitter', user=test_user)
    return test_link