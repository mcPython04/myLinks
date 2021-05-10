from django import urls
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from links.models import link
import pytest


@pytest.mark.django_db
def test_link_set_true(client, create_test_link):
    assert User.objects.count() == 1
    assert link.objects.count() == 1
    test_link = create_test_link
    client.force_login(test_link.user)
    client.post('updateLink', data={'d_id': test_link.id, 'set': "Set", 'type': 'Default', 'user': test_link.user})
    assert test_link.default == True

