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
def test_home_view(client, create_test_user):
    test_user = create_test_user
    client.force_login(test_user)
    resp = client.get(reverse('home'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_update_link_set_default_true(client, create_test_link):
    test_link = create_test_link
    client.force_login(test_link.user)
    form = UpdateLinkSetDefaultForm(data={'d_id': test_link.id, 'set': 'Set', 'type': 'Default'})
    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.default == True


@pytest.mark.django_db
def test_update_link_set_default_false(client, create_test_link):
    test_link = create_test_link
    test_link.default = True
    client.force_login(test_link.user)
    form = UpdateLinkRemoveDefaultForm(data={'d_id': test_link.id, 'set': 'Remove', 'type': 'Default'})
    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.default == False


@pytest.mark.django_db
def test_update_link_set_enable_false(client, create_test_link):
    test_link = create_test_link
    client.force_login(test_link.user)
    form = UpdateLinkDisableForm(data={'d_id': test_link.id, 'set': 'Disable', 'type': 'Enable'})
    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.enabled == False


@pytest.mark.django_db
def test_update_link_set_enable_true(client, create_test_link):
    test_link = create_test_link
    test_link.enabled = False
    client.force_login(test_link.user)
    form = UpdateLinkDisableForm(data={'d_id': test_link.id, 'set': 'Set', 'type': 'Enable'})
    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.enabled == True


@pytest.mark.django_db
def test_link_create_view(client, create_test_user):
    user = create_test_user
    client.force_login(user)
    lcv = LinkCreateView()
    form = lcv.get_form_class()
    newphoto = SimpleUploadedFile(name='test_image.jpg', content=open('links/tests/test_data/background.jpg', 'rb').read(),
                                  content_type='image/jpeg')
    form = form(data={'hyperlink': 'https://twitter.com/', 'website_name': 'Twitter', 'image': newphoto})
    req = client.post(reverse('createLink'), data=form.data)
    assert req.status_code == 302
    assert link.objects.count() == 1


@pytest.mark.django_db
def test_link_delete_view(client, create_test_link):
    test_link = create_test_link
    test_user = test_link.user
    assert User.objects.count() == 1
    assert link.objects.count() == 1
    client.force_login(test_user)
    resp = client.get(reverse('deleteLink', kwargs={'pk': 1}))
    assert resp.status_code == 200
    resp1 = client.post(reverse('deleteLink', kwargs={'pk': 1}))
    assert resp1.status_code == 302
    assert User.objects.count() == 1
    assert link.objects.count() == 0


@pytest.mark.django_db
def test_collection_detail_view(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user
    assert User.objects.count() == 1
    assert collection.objects.count() == 1
    assert link.objects.count() == 1
    client.force_login(test_user)
    resp = client.get(reverse('detailCollection', kwargs={'pk': 1}))
    assert resp.status_code == 200
    assert User.objects.count() == 1
    assert collection.objects.count() == 1
    assert link.objects.count() == 1


@pytest.mark.django_db
def test_collection_delete_view(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    resp = client.get(reverse('deleteCollection', kwargs={'pk': 1}))
    assert resp.status_code == 200
    resp1 = client.post(reverse('deleteCollection', kwargs={'pk': 1}))
    assert resp1.status_code == 302
    assert collection.objects.count() == 0


@pytest.mark.django_db
def test_collection_link_delete_view(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    resp = client.post(reverse('removeLink', kwargs={'pk': 1}), data={'link_id': test_collection.links.get(pk=1).id})
    assert resp.status_code == 302
    assert test_collection.links.all().count() == 0


@pytest.mark.django_db
def test_user_page(client, create_test_user):
    test_user = create_test_user
    resp = client.get(reverse('userPage', kwargs={'username': test_user.username}))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_no_user_page(client):
    resp = client.get(reverse('userPage', kwargs={'username': 'testing123'}))
    assert resp.status_code == 404


@pytest.mark.django_db
def test_collection_page(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user

    resp = client.get(reverse('collectionPage', kwargs={'username': test_user.username, 'collection_name': test_collection.name}))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_collection_page_no_collection(client, create_test_user):
    test_user = create_test_user
    resp = client.get(reverse('collectionPage', kwargs={'username': test_user.username, 'collection_name': 'abc'}))
    assert resp.status_code == 404


@pytest.mark.django_db
def test_collection_page_no_user(client):
    resp = client.get(reverse('collectionPage', kwargs={'username': 'testing123', 'collection_name': 'abc'}))
    assert resp.status_code == 404


@pytest.mark.django_db
def test_collection_create_view(client, create_test_links):
    links = create_test_links(3)
    test_user = links[0].user
    # test_collection = create_test_collection
    # test_user = test_collection.user
    # test_link = test_collection.links.get(pk=1)
    client.force_login(test_user)
    # ccv = CollectionCreateView()
    # form = ccv.get_form_class()
    # import pdb;pdb.set_trace()
    # form = form(data={'name': 'abc', 'user': test_user})
    # form.links.set(test_link)

    req = client.post(reverse('createCollection'), data={'name': 'abc', 'user': test_user, 'links': [link.id for link
                                                                                                     in links]})
    assert req.status_code == 302
    assert collection.objects.count() == 1


@pytest.mark.django_db
def test_collection_update_view_remove_link(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    req = client.post(reverse('updateCollection', kwargs={'pk': test_collection.id}), data={})
    assert req.status_code == 302
    test_collection = collection.objects.get(id=test_collection.id)
    assert test_collection.links.all().count() == 0


@pytest.mark.django_db
def test_link_upload_view(client, create_test_link_with_image):
    test_link = create_test_link_with_image
    test_user = test_link.user
    client.force_login(test_user)
    newphoto = SimpleUploadedFile(name='test_image.jpg',
                                  content=open('links/tests/test_data/amazon.jpg', 'rb').read(),
                                  content_type='image/jpeg')
    req = client.post(reverse('uploadLink', kwargs={'pk': 1}), data={'image': newphoto})
    assert req.status_code == 302
    assert link.objects.count() == 1
    assert User.objects.count() == 1
