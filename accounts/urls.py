# from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_view

from .views import LoginView, LogoutView, RegisterView, send_email_verification_code, EmailVerificationView

urlpatterns = [
    path('login/', LoginView.as_view(), name='accounts_login'),
    path('logout/', LogoutView.as_view(), name='accounts_logout'),
    path('register/', RegisterView.as_view(), name='accounts_register'),
    path('send_email_verification_code/', send_email_verification_code, name='accounts_send_email_verification_code'),
    path('verify_email/', EmailVerificationView.as_view(), name='accounts_email_verification'),
    path('password_change/',
         auth_view.PasswordChangeView.as_view(template_name='accounts/password_change_form.html',
                                              success_url=reverse_lazy('accounts_password_change_done')),
         name='accounts_password_change'),
    path('password_change/done/',
         auth_view.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='accounts_password_change_done'),
]
