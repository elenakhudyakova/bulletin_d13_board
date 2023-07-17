from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm, EmailVerificationForm
from .models import User, EmailVerificationCode


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        default_response = super().form_valid(form)

        if not form.get_user().email_verified:
            return redirect(reverse('accounts_email_verification'))

        return default_response


class LogoutView(BaseLogoutView):
    template_name = 'accounts/logout.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts_login')


@require_POST
@login_required
def send_email_verification_code(request, *args, **kwargs):
    if not request.user.email_verified:
        code, created = EmailVerificationCode.objects.get_or_create(user=request.user)
        if not created:
            code.generate_new_code()

    return redirect(reverse('accounts_email_verification'))


class EmailVerificationView(LoginRequiredMixin, generic.FormView):
    form_class = EmailVerificationForm
    template_name = 'accounts/email_verification.html'
    success_url = reverse_lazy('board_index')

    def dispatch(self, request, *args, **kwargs):
        if getattr(request.user, 'email_verified', False):
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['code'] = EmailVerificationCode.objects.filter(user=self.request.user).first()
        return context

    def form_valid(self, form):
        code = EmailVerificationCode.objects.filter(user=self.request.user).first()
        if code is None:
            context = self.get_context_data(form=form)
            context['code_incorrect'] = "Sorry, we can't find your code."
            return self.render_to_response(context)

        if code.check_time():
            context = self.get_context_data(form=form)
            context['code_incorrect'] = "Your code is out of time."
            return self.render_to_response(context)

        user = self.request.user
        if form.cleaned_data['code'] != code.code:
            context = self.get_context_data(form=form)
            context['code_incorrect'] = "Code incorrect"
            return self.render_to_response(context)

        user.email_verified = True
        user.save()
        code.delete()
        return super().form_valid(form)




