from django.urls import path, include

from apps.organizations.views import (
    MainTemplateView,
    EmployeesListView, EmployeesCreateView, EmployeeImportView,
    EmployeeEditView, DownloadEmployeesExcelView,
    FilialsListView, FilialDetailView, FilialCreateView,
    FilialAddAdminView,
    DepartmentsListView, DepartmentCreateView, DepartmentDetailView,
    DepartmentListByFilialView,
    ReportsListView, ReportDetailView, ReportDownloadView, ReportPrintView,
    ReportsDownloadView,
    OrganizationSettingView, QrCodeDownloadView,
    TariffTemplateView, FeedbackCreateView, TariffPackagesListView,
    GlobalUserSearchView,
    UserOrgView,
)


app_name = 'organizations'

employees_urls = [
    path('', EmployeesListView.as_view(), name='employees_list'),
    path('create', EmployeesCreateView.as_view(), name='employee_create'),
    path('import', EmployeeImportView.as_view(), name='employees_import'),
    path('<int:user_org_pk>/edit',
         EmployeeEditView.as_view(), name='employee_edit'),
    path('download-template',
         DownloadEmployeesExcelView.as_view(), name='download_template'),
]
reports_urls = [
    path('', ReportsListView.as_view(), name='reports_list'),
    path('download/', ReportsDownloadView.as_view(), name='reports_download'),
    path('<int:user_org_id>/', include([
        path('', ReportDetailView.as_view(), name='report_detail'),
        path('download/', ReportDownloadView.as_view(), name='report_download'),
        path('print/', ReportPrintView.as_view(), name='report_print'),
    ])),
]
departments_urls = [
    path('', DepartmentsListView.as_view(), name='departments_list'),
    path('create', DepartmentCreateView.as_view(), name='department_create'),
    path('<int:depart_pk>',
         DepartmentDetailView.as_view(), name='department_detail'),
]
filials_urls = [
    path('', FilialsListView.as_view(), name='filials_list'),
    path('create', FilialCreateView.as_view(), name='filial_create'),
    path('<int:filial_pk>', include([
        path('', FilialDetailView.as_view(), name='filial_detail'),
        path('add-filial-admin/',
             FilialAddAdminView.as_view(), name='filial_add_admin'),
    ])),
]
settings_urls = [
    path('', OrganizationSettingView.as_view(), name='settings'),
    path('qr-code-download/',
         QrCodeDownloadView.as_view(), name='qr_code_download')
]
tariffs_urls = [
    path('', TariffTemplateView.as_view(), name='tariffs'),
    path('tariff_packages/',
         TariffPackagesListView.as_view(), name='tariff_detail'),
]

urlpatterns = [
    path('<int:org_pk>/', include([
        path('main/', MainTemplateView.as_view(), name='main'),
        path('employees/', include(employees_urls)),
        path('filials/', include(filials_urls)),
        path('departments/', include(departments_urls)),
        path('reports/', include(reports_urls)),
        path('settings/', include(settings_urls)),
        path('tariffs/', include(tariffs_urls)),
        path('feedback', FeedbackCreateView.as_view(), name='feedback'),
        path('global-search/',
             GlobalUserSearchView.as_view(), name='global_search_users'),
    ])),
    path('departments-by-filial',
         DepartmentListByFilialView.as_view(), name='departments_list_filial'),
    path('user-orgs', UserOrgView.as_view(), name='user_orgs')
]
