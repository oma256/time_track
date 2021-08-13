from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.services.fabric import ServiceClasses
from apps.users.forms import (
    UserLoginForm,
    UserRegistrationForm,
    ChangePasswordForm,
)


class AbstractFormView(FormView):
    services = ServiceClasses


class UserRegistrationView(AbstractFormView):
    template_name = 'pages/registration.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        data = self.services.user.user_registration(
            request=self.request, form=form
        )
        organization = self.services.organization.create_organization(
            org_name=data.get('org_name'), admin=data.get('user')
        )

        self.services.org_tariff_package.create_org_tariff_package(organization)
        self.services.user_organization.create_user_organization(
            user=data.get('user'), organization=organization, data=data
        )

        return JsonResponse({
            'redirect_url': reverse(
                viewname='organizations:settings', args=(organization.id,),
            )
        })

    def form_invalid(self, form):
        html = render_to_string(
            template_name="components/registration_form.html",
            context={"form": form}, request=self.request,
        )

        return JsonResponse({'html': html}, safe=False, status=400)


class LoginView(AbstractFormView):
    template_name = 'pages/index.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and not user.is_superuser:
            self.success_url = (
                self.services.user.get_login_success_url(
                    user=user
                )
            )
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user, user_org = self.services.user.user_login(
            request=self.request, form=form
        )

        if user:
            self.success_url = (
                self.services.user.get_login_success_url(
                    user_org=user_org, user=user
                )
            )
            return super().form_valid(form)
        return self.render_to_response({'form': form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))


class ForgotPasswordView(AbstractFormView):
    template_name = 'pages/forgot-password.html'
    form_class = ChangePasswordForm

    def form_valid(self, form):
        user = self.services.user.get_user_by_phone_number(
            phone_number=form.cleaned_data.get('phone_number')
        )
        self.services.user.change_user_password(user, form)

        return JsonResponse({'detail': 'success'}, status=200)

    def form_invalid(self, form):
        html = render_to_string(
            template_name="components/change_password_form.html",
            context={"form": form}, request=self.request,
        )

        return JsonResponse({'html': html}, safe=False, status=400)
