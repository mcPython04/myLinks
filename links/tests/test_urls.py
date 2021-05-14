from django.urls import reverse, resolve


# Testing URLs
class TestUrls:

    def test_home_url(self):
        path = reverse('home')
        assert resolve(path).view_name == 'home'

    def test_base_url(self):
        path = reverse('base')
        assert resolve(path).view_name == 'base'

    def test_user_page(self):
        path = reverse('userPage', kwargs={'username': 'random123'})
        assert resolve(path).view_name == 'userPage'

    def test_update_link(self):
        path = reverse('updateLink')
        assert resolve(path).view_name == 'updateLink'

    def test_create_link(self):
        path = reverse('createLink')
        assert resolve(path).view_name == 'createLink'

    def test_create_collection(self):
        path = reverse('createCollection')
        assert resolve(path).view_name == 'createCollection'

    def test_delete_link(self):
        path = reverse('deleteLink', kwargs={'pk': 1})
        assert resolve(path).view_name == 'deleteLink'

    def test_upload_link(self):
        path = reverse('uploadLink', kwargs={'pk': 1})
        assert resolve(path).view_name == 'uploadLink'

    def test_detail_collection(self):
        path = reverse('detailCollection', kwargs={'pk': 1})
        assert resolve(path).view_name == 'detailCollection'

    def test_delete_collection(self):
        path = reverse('deleteCollection', kwargs={'pk': 1})
        assert resolve(path).view_name == 'deleteCollection'

    def test_remove_link(self):
        path = reverse('removeLink', kwargs={'pk': 1})
        assert resolve(path).view_name == 'removeLink'

    def test_update_collection(self):
        path = reverse('updateCollection', kwargs={'pk': 1})
        assert resolve(path).view_name == 'updateCollection'

    def test_collection_page(self):
        path = reverse('collectionPage', kwargs={'collection_name': 'random', 'username': 'random123'})
        assert resolve(path).view_name == 'collectionPage'
