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
                      data={'link_id': test_collection.links.get(pk=1).id})
    assert test_user.username + ' removed a link from his/her collection' in caplog.text
