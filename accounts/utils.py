from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class EmailVerificationRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.email_verified


def verified_email_required(
    function=None, redirect_field_name='next', login_url=None
):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.email_verified,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
