from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.contrib.auth.mixins import AccessMixin
from django.views.decorators.http import require_POST

from accounts.utils import EmailVerificationRequiredMixin
from .forms import AdForm, ReplyForm
from .models import Ad, Reply


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class AdDetail(AccessMixin, generic.DetailView, generic.edit.BaseFormView):
    template_name = 'ad_detail.html'
    model = Ad
    context_object_name = 'ad'
    form_class = ReplyForm

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).select_related('author').defer('author__password')

    def post(self, request, *args, **kwargs):
        if not (self.request.user.is_authenticated and self.request.user.email_verified):
            return self.handle_no_permission()

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        ad = self.get_object()
        reply.ad = ad
        form.save()
        return redirect(reverse('board_sent_replies'))


class AdCreate(EmailVerificationRequiredMixin, generic.CreateView):
    template_name = 'ad_create.html'
    model = Ad
    form_class = AdForm

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.author = self.request.user
        return super().form_valid(form)


class AdUpdate(AccessMixin, generic.UpdateView):
    template_name = 'ad_create.html'
    model = Ad
    form_class = AdForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


@require_POST
def ad_deactivate(request, pk, *args, **kwargs):
    ad = get_object_or_404(
        Ad.objects.select_related('author').defer('content', 'author__password'), pk=pk)

    if request.user != ad.author:
        raise PermissionDenied

    if ad.is_active:
        ad.is_active = False
        ad.save()

    return redirect(reverse('board_user_ads'))


class AdList(generic.ListView):
    template_name = 'ad_list.html'
    model = Ad
    context_object_name = 'ads'
    ordering = '-created_at'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).select_related('author') \
            .defer('content', 'author__password')


class CategoryAdList(AdList):
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdList, self).get_context_data(object_list=object_list, **kwargs)
        context['main_category_pk'] = self.kwargs.get('category_pk')
        return context

    def get_queryset(self):
        category_pk = self.kwargs.get('category_pk')
        return super().get_queryset().filter(category__pk=category_pk, is_active=True).defer('content')


class UserAdList(AdList):
    extra_context = {'title': _('Your ads')}

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class RepliesListView(EmailVerificationRequiredMixin, generic.ListView):
    template_name = 'replies_list.html'
    model = Reply
    context_object_name = 'replies'
    ordering = '-created_at'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(is_accepted=False).select_related('author', 'ad', 'ad__author') \
            .defer('author__password', 'ad__content', 'ad__author__password')


class SentRepliesView(RepliesListView):
    extra_context = {'title': _('Sent replies')}

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class ReceivedRepliesView(RepliesListView):
    extra_context = {'title': _('Received replies')}

    def get_queryset(self):
        ad_pk = self.request.GET.get('ad')
        qs = super().get_queryset().filter(ad__author=self.request.user)
        if ad_pk is None:
            return qs
        else:
            return qs.filter(ad__pk=ad_pk)


@require_POST
def accept_reply(request, pk, **kwargs):
    reply = get_object_or_404(
        Reply.objects.select_related('ad', 'ad__author').defer('ad__content', 'ad__author__password'), pk=pk)

    if request.user != reply.ad.author:
        raise PermissionDenied

    if not reply.is_accepted:
        reply.is_accepted = True
        reply.save(update_fields=('is_accepted',))

    return redirect(reverse('board_received_replies'))


@require_POST
def delete_reply(request, pk, **kwargs):
    reply = get_object_or_404(
        Reply.objects.select_related('ad', 'ad__author').defer('ad__content', 'ad__author__password'), pk=pk)

    if request.user != reply.ad.author:
        raise PermissionDenied

    if not reply.is_accepted:
        reply.delete()

    return redirect(reverse('board_received_replies'))
