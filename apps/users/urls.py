from django.urls import path

from apps.users.views import (
    LoginView, LogoutView, UserRegistrationView, ForgotPasswordView,
)


app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('forgot_password/',
         ForgotPasswordView.as_view(), name='forgot_password'),
]
