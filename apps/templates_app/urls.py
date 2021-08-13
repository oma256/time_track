from django.urls import path

from apps.templates_app import views

app_name = 'templates'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('main-add-staff/', views.MainAddStaffView.as_view(), name='main-add-staff'),
    path('add-employee/', views.AddEmployeeView.as_view(), name='add-employee'),
    path('import-staff/', views.ImportStaffView.as_view(), name='import-staff'),
    path('add-staff/', views.AddStaffView.as_view(), name='add-staff'),
    path('filial/', views.FilialView.as_view(), name='filial'),
    path('filial-detail/', views.FilialDetailView.as_view(), name='filial-detail'),
    path('add-filial/', views.AddFilialView.as_view(), name='add-filial'),
    path('departments/', views.DepartmentsView.as_view(), name='departments'),
    path('departments-detail/', views.DepartmentDetailView.as_view(), name='departments-detail'),
    path('add-departments/', views.AddDepartmentsView.as_view(), name='add-departments'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('tariffs/', views.TariffsView.as_view(), name='tariffs'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('reports-detail/', views.ReportsDetailView.as_view(), name='reports-detail'),
    path('search-result-detail/', views.SearchResultDetailView.as_view(), name='search-result-detail'),
]


