from links.views import *
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_log(client, create_test_user, caplog):
    test_user = create_test_user
    client.force_login(test_user)
    client.get(reverse('home'))
    assert str(test_user) in caplog.text
