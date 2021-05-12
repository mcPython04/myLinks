from django import urls
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from links.models import link
from links.views import *
from links.forms import *
import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


# Home Tests
@pytest.mark.django_db
def test_home_view(client, create_test_user):
    test_user = create_test_user
    client.force_login(test_user)
    req = client.get(reverse('home'))
    assert req.status_code == 200


# User Page tests
@pytest.mark.django_db
def test_user_page(client, create_test_user):
    test_user = create_test_user
    req = client.get(reverse('userPage', kwargs={'username': test_user.username}))
    assert req.status_code == 200


@pytest.mark.django_db
def test_no_user_page(client):
    req = client.get(reverse('userPage', kwargs={'username': 'testing123'}))
    assert req.status_code == 404


# Collection Page tests
@pytest.mark.django_db
def test_collection_page(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user

    req = client.get(reverse('collectionPage', kwargs={'username': test_user.username,
                                                       'collection_name': test_collection.name}))
    assert req.status_code == 200


@pytest.mark.django_db
def test_collection_page_no_collection(client, create_test_user):
    test_user = create_test_user
    req = client.get(reverse('collectionPage', kwargs={'username': test_user.username,
                                                       'collection_name': 'abc'}))
    assert req.status_code == 404


@pytest.mark.django_db
def test_collection_page_no_user(client):
    req = client.get(reverse('collectionPage', kwargs={'username': 'testing123',
                                                       'collection_name': 'abc'}))
    assert req.status_code == 404


# Base view tests
@pytest.mark.django_db
def test_base_view(client, create_test_user):
    test_user = create_test_user
    client.force_login(test_user)
    req = client.get(reverse('base'))
    assert req.status_code == 200


# Link Update View tests
@pytest.mark.django_db
def test_update_link_set_default_true(client, create_test_link):
    test_link = create_test_link
    client.force_login(test_link.user)
    form = UpdateLinkSetDefaultForm(data={'d_id': test_link.id,
                                          'set': 'Set',
                                          'type': 'Default'})

    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.default == True


@pytest.mark.django_db
def test_update_link_set_default_false(client, create_test_link):
    test_link = create_test_link
    test_link.default = True
    client.force_login(test_link.user)
    form = UpdateLinkRemoveDefaultForm(data={'d_id': test_link.id,
                                             'set': 'Remove',
                                             'type': 'Default'})

    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.default == False


@pytest.mark.django_db
def test_update_link_set_enable_false(client, create_test_link):
    test_link = create_test_link
    client.force_login(test_link.user)
    form = UpdateLinkDisableForm(data={'d_id': test_link.id,
                                       'set': 'Disable',
                                       'type': 'Enable'})

    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.enabled == False


@pytest.mark.django_db
def test_update_link_set_enable_true(client, create_test_link):
    test_link = create_test_link
    test_link.enabled = False
    client.force_login(test_link.user)
    form = UpdateLinkDisableForm(data={'d_id': test_link.id,
                                       'set': 'Set',
                                       'type': 'Enable'})

    req = client.post(reverse('updateLink'), data=form.data)
    assert req.status_code == 302
    test_link = link.objects.get(id=test_link.id)
    assert test_link.enabled == True


# Link Create View tests
@pytest.mark.django_db
def test_link_create_view(client, create_test_user):
    user = create_test_user
    client.force_login(user)
    lcv = LinkCreateView()
    form = lcv.get_form_class()
    new_photo = SimpleUploadedFile(name='test_image.jpg',
                                   content=open('links/tests/test_data/background.jpg', 'rb').read(),
                                   content_type='image/jpeg')

    form = form(data={'hyperlink': 'https://twitter.com/',
                      'website_name': 'Twitter',
                      'image': new_photo})

    req = client.post(reverse('createLink'), data=form.data)
    assert req.status_code == 302
    assert link.objects.count() == 1


# Link Delete View tests
@pytest.mark.django_db
def test_link_delete_view(client, create_test_link):
    test_link = create_test_link
    test_user = test_link.user
    assert User.objects.count() == 1
    assert link.objects.count() == 1
    client.force_login(test_user)
    req = client.get(reverse('deleteLink', kwargs={'pk': test_link.id}))
    assert req.status_code == 200
    req1 = client.post(reverse('deleteLink', kwargs={'pk': test_link.id}))
    assert req1.status_code == 302
    assert User.objects.count() == 1
    assert link.objects.count() == 0


# Link Upload View tests
@pytest.mark.django_db
def test_link_upload_view(client, create_test_link_with_image):
    test_link = create_test_link_with_image
    test_user = test_link.user
    client.force_login(test_user)
    new_photo = SimpleUploadedFile(name='test_image.jpg',
                                   content=open('links/tests/test_data/amazon.jpg', 'rb').read(),
                                   content_type='image/jpeg')

    req = client.post(reverse('uploadLink', kwargs={'pk': test_link.id}), data={'image': new_photo})
    assert req.status_code == 302
    assert link.objects.count() == 1
    assert User.objects.count() == 1


# Collection Create View tests
@pytest.mark.django_db
def test_collection_create_view_with_multiple_links(client, create_test_links):
    links = create_test_links(3)
    test_user = links[0].user
    client.force_login(test_user)

    req = client.post(reverse('createCollection'), data={'name': 'abc',
                                                         'user': test_user,
                                                         'links': [link.id for link in links]})
    assert req.status_code == 302
    assert collection.objects.count() == 1


@pytest.mark.django_db
def test_collection_create_view_with_no_links(client, create_test_user):
    test_user = create_test_user
    client.force_login(test_user)
    req = client.post(reverse('createCollection'), data={'name': 'abc',
                                                         'user': test_user})
    assert req.status_code == 302
    assert collection.objects.count() == 1


@pytest.mark.django_db
def test_collection_create_view_with_one_links(client, create_test_links):
    links = create_test_links(1)
    test_user = links[0].user
    client.force_login(test_user)
    req = client.post(reverse('createCollection'), data={'name': 'abc',
                                                         'user': test_user,
                                                         'links': [link.id for link in links]})
    assert req.status_code == 302
    assert collection.objects.count() == 1


# Collection Detail View tests
@pytest.mark.django_db
def test_collection_detail_view(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user
    assert User.objects.count() == 1
    assert collection.objects.count() == 1
    assert link.objects.count() == 1
    client.force_login(test_user)
    req = client.get(reverse('detailCollection', kwargs={'pk': test_collection.id}))
    assert req.status_code == 200
    assert User.objects.count() == 1
    assert collection.objects.count() == 1
    assert link.objects.count() == 1


# Collection Delete View tests
@pytest.mark.django_db
def test_collection_delete_view(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    req = client.get(reverse('deleteCollection', kwargs={'pk': test_collection.id}))
    assert req.status_code == 200
    req1 = client.post(reverse('deleteCollection', kwargs={'pk': test_collection.id}))
    assert req1.status_code == 302
    assert collection.objects.count() == 0


# Collection Update View tests
@pytest.mark.django_db
def test_collection_update_view_remove_link(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    req = client.post(reverse('updateCollection', kwargs={'pk': test_collection.id}), data={})
    assert req.status_code == 302
    test_collection = collection.objects.get(id=test_collection.id)
    assert test_collection.links.all().count() == 0


# Collection Link Delete View tests
@pytest.mark.django_db
def test_collection_link_delete_view(client, create_test_collection):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    req = client.post(reverse('removeLink', kwargs={'pk': test_collection.id}),
                      data={'link_id': test_collection.links.get(pk=1).id})
    assert req.status_code == 302
    assert test_collection.links.all().count() == 0



