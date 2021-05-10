from django import urls
from django.contrib.auth import get_user_model
import pytest


@pytest.mark.parametrize('param', [
    ('home'),
    ('base'),
    ('userPage'),
    ('updateLink'),
    ('createLink'),
    ('createCollection'),
    ('deleteLink'),
    ('uploadLink'),
    ('detailCollection'),
    ('deleteCollection'),
    ('removeLink'),
    ('updateCollection'),
    ('collectionPage'),
])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200
