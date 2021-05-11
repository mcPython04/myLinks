from django import urls
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from links.models import link
from links.views import *
from links.forms import *
import pytest


@pytest.mark.django_db
def test_link_set_true(client, create_test_link):
    assert User.objects.count() == 1
    assert link.objects.count() == 1
    test_link = create_test_link
    client.force_login(test_link.user)
    form = UpdateLinkSetDefaultForm(data={'d_id': test_link.id, 'set': "Set", 'type': 'Default'})
    #import pdb; pdb.set_trace()
    req = client.post('/links/update', data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.default == True

#django.forms.widgets.linkForm
@pytest.mark.django_db
def test_link_create_view():
    lcv = LinkCreateView()
    form = lcv.get_form_class(data={'hyperlink': , 'website_name': , 'image': 'Default'})

    import pdb;pdb.set_trace()
    pass

