from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'pages/index.html'


class MainAddStaffView(TemplateView):
    template_name = 'pages/main/main-add-staff.html'


class AddEmployeeView(TemplateView):
    template_name = 'pages/employees/add__employee.html'


class ImportStaffView(TemplateView):
    template_name = 'pages/employees/import-staff.html'


class AddStaffView(TemplateView):
    template_name = 'pages/employees/add__staff.html'


class FilialView(TemplateView):
    template_name = 'pages/filials/filial.html'


class FilialDetailView(TemplateView):
    template_name = 'pages/filials/filial-detail.html'


class AddFilialView(TemplateView):
    template_name = 'pages/filials/add-filial.html'


class DepartmentsView(TemplateView):
    template_name = 'pages/departments/departments.html'


class DepartmentDetailView(TemplateView):
    template_name = 'pages/departments/departments-detail.html'


class AddDepartmentsView(TemplateView):
    template_name = 'pages/departments/add-departments.html'


class SettingsView(TemplateView):
    template_name = 'pages/settings/settings.html'


class TariffsView(TemplateView):
    template_name = 'pages/tariffs.html'


class ReportsView(TemplateView):
    template_name = 'pages/reports/reports.html'


class ReportsDetailView(TemplateView):
    template_name = 'pages/reports/reports-detail.html'


class SearchResultDetailView(TemplateView):
    template_name = 'pages/search-result-detail.html'
