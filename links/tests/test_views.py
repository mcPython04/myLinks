from django import urls
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from links.models import link
from links.views import *
from links.forms import *
import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_link_set_true(client, create_test_link):
    assert User.objects.count() == 1
    assert link.objects.count() == 1
    test_link = create_test_link
    client.force_login(test_link.user)
    form = UpdateLinkSetDefaultForm(data={'d_id': test_link.id, 'set': "Set", 'type': 'Default'})
    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.default == True


#django.forms.widgets.linkForm
@pytest.mark.django_db
def test_link_create_view(client, create_test_user):
    user = create_test_user
    client.force_login(user)
    lcv = LinkCreateView()
    form = lcv.get_form_class()
    newphoto = SimpleUploadedFile(name='test_image.jpg', content=open('/home/ldoan/Downloads/background.jpg', 'rb').read(),
                                        content_type='image/jpeg')
    form = form(data={'hyperlink': 'https://twitter.com/', 'website_name': 'Twitter', 'image': newphoto})
    req = client.post(reverse('createLink'), data=form.data)
    #import pdb;pdb.set_trace()
    assert req.status_code == 302
    assert link.objects.count() == 1

