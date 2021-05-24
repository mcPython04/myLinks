from links.views import *
import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_login_success(client, create_test_user, caplog):
    test_user = create_test_user
    client.force_login(test_user)
    assert test_user.username + ' logged in via ip: ' in caplog.text


@pytest.mark.django_db
def test_login_fail(client, create_test_user_with_password, caplog):
    test_user = create_test_user_with_password
    username = test_user.username
    client.post('/accounts/login/', {'username': username, 'password': 'test1234'})
    assert 'login failed for: ' in caplog.text
    assert 'via ip: ' in caplog.text


@pytest.mark.django_db
def test_logout(client, create_test_user, caplog):
    test_user = create_test_user
    username = test_user.username
    client.force_login(test_user)
    client.logout()
    assert username + ' logged out via ip: ' in caplog.text


@pytest.mark.django_db
def test_home(client, create_test_user, caplog):
    test_user = create_test_user
    username = test_user.username
    client.force_login(test_user)
    client.get(reverse('home'))
    assert username + ' visited the home page' in caplog.text


@pytest.mark.django_db
def test_user_page_exist(client, create_test_user, caplog):
    test_user = create_test_user
    username = test_user.username
    client.force_login(test_user)
    client.get(reverse('userPage', kwargs={'username': username}))
    assert username + ' visited ' + username + '\'s page' in caplog.text


@pytest.mark.django_db
def test_user_page_not_exist(client, create_test_user, caplog):
    test_user = create_test_user
    username = test_user.username
    client.force_login(test_user)
    client.get(reverse('userPage', kwargs={'username': 'testing123'}))
    assert username + ' tried to visit a user\'s page that did not exist' in caplog.text


@pytest.mark.django_db
def test_collection_page_user_not_exist(client, create_test_user, caplog):
    test_user = create_test_user
    username = test_user.username
    client.force_login(test_user)
    client.get(reverse('collectionPage', kwargs={'username': 'test123', 'collection_name': 'Test collection1'}))
    assert username + ' tried to visit a user\'s collection page but the user did not exist' in caplog.text


@pytest.mark.django_db
def test_collection_page_collection_exist(client, create_test_collection, caplog):
    test_collection = create_test_collection
    test_user = test_collection.user
    username = test_user.username
    collection_name = test_collection.name
    client.force_login(test_user)
    client.get(reverse('collectionPage', kwargs={'username': 'test_user3', 'collection_name': 'Test collection1'}))
    assert username + ' visited ' + username + '\'s ' + collection_name + ' collection' in caplog.text


@pytest.mark.django_db
def test_collection_page_collection_not_exist(client, create_test_user, caplog):
    test_user = create_test_user
    username = test_user.username
    client.force_login(test_user)
    client.get(reverse('collectionPage', kwargs={'username': username, 'collection_name': 'Test collection1'}))
    assert username + ' tried to visit ' + username + '\'s collection that did not exist' in caplog.text


@pytest.mark.django_db
def test_link_create_form_valid(client, create_test_user, caplog):
    user = create_test_user
    username = user.username
    client.force_login(user)
    lcv = LinkCreateView()
    form = lcv.get_form_class()
    new_photo = SimpleUploadedFile(name='test_image.jpg',
                                   content=open('links/tests/test_data/background.jpg', 'rb').read(),
                                   content_type='image/jpeg')

    form = form(data={'hyperlink': 'https://twitter.com/',
                      'website_name': 'Twitter',
                      'image': new_photo})

    client.post(reverse('createLink'), data=form.data)
    assert username + ' created a link' in caplog.text


@pytest.mark.django_db
def test_link_delete_view(client, create_test_link, caplog):
    test_link = create_test_link
    test_user = test_link.user
    client.force_login(test_user)
    client.get(reverse('deleteLink', kwargs={'pk': test_link.id}))
    client.post(reverse('deleteLink', kwargs={'pk': test_link.id}))
    assert test_user.username + ' deleted a link' in caplog.text


@pytest.mark.django_db
def test_link_upload_view(client, create_test_link_with_image, caplog):
    test_link = create_test_link_with_image
    test_user = test_link.user
    client.force_login(test_user)
    new_photo = SimpleUploadedFile(name='test_image.jpg',
                                   content=open('links/tests/test_data/amazon.jpg', 'rb').read(),
                                   content_type='image/jpeg')

    client.post(reverse('uploadLink', kwargs={'pk': test_link.id}), data={'image': new_photo})
    assert test_user.username + ' updated a link\'s image' in caplog.text


@pytest.mark.django_db
def test_log_collection_create_view_with_multiple_links(client, create_test_links, caplog):
    links = create_test_links(3)
    test_user = links[0].user
    client.force_login(test_user)

    client.post(reverse('createCollection'), data={'name': 'abc',
                                                   'user': test_user,
                                                   'links': [link.id for link in links]})
    assert test_user.username + ' created a collection' in caplog.text


@pytest.mark.django_db
def test_log_collection_create_view_with_no_links(client, create_test_user, caplog):
    test_user = create_test_user
    client.force_login(test_user)
    client.post(reverse('createCollection'), data={'name': 'abc',
                                                   'user': test_user})
    assert test_user.username + ' created a collection' in caplog.text


@pytest.mark.django_db
def test_log_collection_create_view_with_one_links(client, create_test_links, caplog):
    links = create_test_links(1)
    test_user = links[0].user
    client.force_login(test_user)
    client.post(reverse('createCollection'), data={'name': 'abc',
                                                   'user': test_user,
                                                   'links': [link.id for link in links]})
    assert test_user.username + ' created a collection' in caplog.text


@pytest.mark.django_db
def test_log_collection_detail_view(client, create_test_collection, caplog):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    client.get(reverse('detailCollection', kwargs={'pk': test_collection.id}))
    assert test_user.username + ' looked at a collection' in caplog.text


@pytest.mark.django_db
def test_log_collection_delete_view_(client, create_test_collection, caplog):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    client.post(reverse('deleteCollection', kwargs={'pk': test_collection.id}))
    assert test_user.username + ' deleted a collection' in caplog.text


@pytest.mark.django_db
def test_log_collection_update_view_remove_link(client, create_test_collection, caplog):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    client.post(reverse('updateCollection', kwargs={'pk': test_collection.id}), data={})
    assert test_user.username + ' updated a collection' in caplog.text


@pytest.mark.django_db
def test_log_collection_link_delete_view(client, create_test_collection, caplog):
    test_collection = create_test_collection
    test_user = test_collection.user
    client.force_login(test_user)
    client.post(reverse('removeLink', kwargs={'pk': test_collection.id}),
                        data={'link_id': test_collection.links.all()[:1].get().id})
    assert test_user.username + ' removed a link from his/her collection' in caplog.text
