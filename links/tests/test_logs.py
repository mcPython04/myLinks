from links.views import *
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_log(client, create_test_user, caplog):
    test_user = create_test_user
    client.force_login(test_user)
    assert test_user.username + ' logged in via ip: ' in caplog.text
    client.get(reverse('home'))
    assert test_user.username + ' visited the home page' in caplog.text


@pytest.mark.django_db
def test_home_log_fail(client, create_test_user_with_password, caplog):
    test_user = create_test_user_with_password
    username = test_user.username
    client.post('/accounts/login/', {'username': username, 'password': 'test1234'})
    assert 'login failed for: ' in caplog.text
    assert 'via ip: ' in caplog.text
