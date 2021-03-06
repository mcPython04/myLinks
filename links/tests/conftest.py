import pytest
from django.contrib.auth.models import User
from links.models import link, collection
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture()
def create_test_user():
    test_user = User.objects.create_user('test_user')
    return test_user


@pytest.fixture()
def create_test_user_with_password():
    test_user = User.objects.create(username='test_user', password='test123')
    return test_user


@pytest.fixture()
def create_test_link():
    test_user = User.objects.create_user('test_user2')
    test_link = link.objects.create(hyperlink='https://twitter.com',
                                    website_name='Twitter',
                                    user=test_user)
    return test_link


@pytest.fixture()
def create_test_collection():
    test_user = User.objects.create_user('test_user3')
    new_photo = SimpleUploadedFile(name='test_image.jpg',
                                   content=open('links/tests/test_data/background.jpg', 'rb').read(),
                                   content_type='image/jpeg')

    link.objects.create(hyperlink='https://twitter.com',
                        website_name='Twitter',
                        user=test_user,
                        image=new_photo)

    get_link = link.objects.all()
    test_collection = collection.objects.create(name='Test collection1',
                                                user=test_user)
    test_collection.links.set(get_link)
    return test_collection


@pytest.fixture
def create_test_links(create_test_user):
    test_user = create_test_user

    def create_link(num_links):
        links = []
        for i in range(num_links):
            links.append(link.objects.create(hyperlink='https://twitter.com',
                                             website_name='Twitter',
                                             user=test_user))
        return links

    return create_link


@pytest.fixture
def create_test_link_with_image(create_test_user):
    test_user = create_test_user

    new_photo = SimpleUploadedFile(name='test_image.jpg',
                                   content=open('links/tests/test_data/background.jpg', 'rb').read(),
                                   content_type='image/jpeg')

    test_link = link.objects.create(hyperlink='https://twitter.com',
                                    website_name='Twitter',
                                    user=test_user,
                                    image=new_photo)
    return test_link
