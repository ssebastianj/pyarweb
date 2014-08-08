from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from community.tests import PermissionMixinTest

from .models import Job
from .forms import JobForm


class JobTest(PermissionMixinTest, TestCase):

    """ Job model tests. """

    def setUp(self):
        self.model = Job
        super(JobTest, self).setUp()

    def test_str(self):
        job = Job(title='Python job')

        self.assertEqual(str(job), 'Python job')

    def test_job_update_view(self):
        self.try_action_with_ownership('jobs_update')

    def test_job_delete_view(self):
        self.try_action_with_ownership('jobs_delete')


class JobListTest(TestCase):

    """ Jobs list view tests. """

    def setUp(self):
        self.u1 = User.objects.create(username='user1')

    def tearDown(self):
        self.u1.delete()

    def test_jobs_in_context(self):
        url = reverse('jobs_list_all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['object_list']), [])

        job = Job.objects.create(owner=self.u1)
        job.tags.add('tag1')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)
        self.assertEqual(response.context['tags'].count(), 1)
