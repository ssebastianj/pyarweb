from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from .models import Job
from .forms import JobForm


class JobTest(TestCase):

    """ Job model tests. """

    def try_action_with_ownership(self, url_name):
        job = Job.objects.create(title='Python job', owner=self.u2)

        url = reverse(url_name, args=(job.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        job.owner = self.u1
        job.save()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.u1 = User.objects.create_user(username='user1', password='pass')
        self.u2 = User.objects.create_user(username='user2', password='pass')
        self.client.login(username='user1', password='pass')

    def tearDown(self):
        self.u1.delete()
        self.u2.delete()

    def test_str(self):
        job = Job(title='Python job')

        self.assertEqual(str(job), 'Python job')

    def test_job_update_view(self):
        self.try_action_with_ownership('jobs_update')

    def test_job_delete_view(self):
        self.try_action_with_ownership('jobs_update')


class JobListTest(TestCase):

    """ Jobs list view tests. """

    def setUp(self):
        self.u1 = User.objects.create(username='user1')

    def tearDown(self):
        self.u1.delete()

    def test_jobs_in_context(self):
        url = reverse('jobs_list_all')
        response = self.client.get(url)
        self.assertEqual(list(response.context['object_list']), [])

        Job.objects.create(owner=self.u1)

        response = self.client.get(url)
        self.assertEqual(response.context['object_list'].count(), 1)
