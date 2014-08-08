from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from community.mixins import PermissionMixin, FilterableListMixin
from .models import Job
from .forms import JobForm


class JobCreate(CreateView):
    model = Job
    form_class = JobForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(JobCreate, self).form_valid(form)


class JobList(FilterableListMixin, ListView):
    model = Job
    paginate_by = 20


class JobUpdate(PermissionMixin, UpdateView):

    """Edit jobs that use Python."""
    model = Job
    form_class = JobForm


class JobDelete(PermissionMixin, DeleteView):

    """Delete a Job."""
    model = Job
    success_url = reverse_lazy('jobs_list_all')
