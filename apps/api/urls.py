from django.urls import path

from apps.api.views import (
    LoginAPIView,
    UserOrganizationListAPIView,
    UserOrganizationDetailAPIView,
    WorkTimeListAPIView,
    VersionRetrieveView,
)


urlpatterns = [
    path('version/', VersionRetrieveView.as_view(), name='app_version'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('user-organizations/',
         UserOrganizationListAPIView.as_view(), name='user_orgs_list'),
    path('user-organizations/<int:pk>/',
         UserOrganizationDetailAPIView.as_view(), name='user_orgs_detail'),
    path('user-organizations/<int:pk>/worktimes/',
         WorkTimeListAPIView.as_view(), name='worktimes_list'),
]
