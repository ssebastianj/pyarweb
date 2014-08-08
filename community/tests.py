from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PermissionMixinTest(object):

    def setUp(self):
        self.u1 = User.objects.create_user(username='user1', password='pass')
        self.u2 = User.objects.create_user(username='user2', password='pass')
        self.client.login(username='user1', password='pass')

    def tearDown(self):
        self.u1.delete()
        self.u2.delete()

    def try_action_with_ownership(self, url_name):
        obj = self.model.objects.create(owner=self.u2)

        url = reverse(url_name, args=(obj.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        obj.owner = self.u1
        obj.save()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
