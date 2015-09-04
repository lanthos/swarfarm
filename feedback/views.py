from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q

from .forms import IssueForm, IssueUpdateStatusForm, CommentForm
from .models import Issue, Discussion


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ProfileNameMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ProfileNameMixin, self).get_context_data(**kwargs)
        context['profile_name'] = self.request.user.username
        return context


class IssueList(LoginRequiredMixin, ProfileNameMixin, ListView):
    model = Issue

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Issue.objects.all()
        else:
            return Issue.objects.filter(Q(user=self.request.user) | Q(public=True))


class IssueCreate(LoginRequiredMixin, ProfileNameMixin, CreateView):
    model = Issue
    form_class = IssueForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = Issue.STATUS_UNREVIEWED
        return super(IssueCreate, self).form_valid(form)


class IssueDetail(LoginRequiredMixin, ProfileNameMixin, DetailView):
    model = Issue

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.user == self.request.user or issue.public or self.request.user.is_superuser:
            return super(IssueDetail, self).get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        comment_form = CommentForm()
        comment_form.helper.form_action = reverse('feedback:comment_add', kwargs={'issue_pk': self.kwargs['pk']})
        context['comment_form'] = comment_form

        if self.request.user.is_superuser:
            status_form = IssueUpdateStatusForm(instance=self.object)
            status_form.helper.form_action = reverse('feedback:issue_status_update', kwargs={'pk': self.kwargs['pk']})
            context['status_form'] = status_form

        return context


class IssueUpdateStatus(LoginRequiredMixin, ProfileNameMixin, UpdateView):
    model = Issue
    form_class = IssueUpdateStatusForm

    def get_success_url(self):
        print 'success hurr durr'
        return reverse('feedback:issue_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreate(LoginRequiredMixin, ProfileNameMixin, CreateView):
    model = Discussion
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.feedback = Issue.objects.get(pk=self.kwargs['issue_pk'])
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('feedback:issue_detail', kwargs={'pk': self.kwargs['issue_pk']})
