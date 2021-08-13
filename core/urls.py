from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from django.views.generic import RedirectView

from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('',
         RedirectView.as_view(url=reverse_lazy('users:login')), name='index'),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(
        title='WorkTime API docs',
        schema_url=f'{settings.SITE_PROTOCOL}{settings.SITE_DOMAIN}'),
    ),
    path('', include('apps.users.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('payment/', include('apps.payment.urls')),

    re_path('api/(?P<version>(v1|v2))/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
