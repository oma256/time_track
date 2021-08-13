from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView

from apps.organizations.forms import FeedbackForm
from apps.services.fabric import ServiceClasses


# Abstract (Class Based View)
class AbstractTemplateView(LoginRequiredMixin, TemplateView):
    services = ServiceClasses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org_pk = kwargs.get('org_pk')
        context['organization'] = (
            self.services.organization.get_organization_by_id(org_id=org_pk)
        )
        context['setting'] = (
            self.services.organization_setting.get_setting_by_org_id(
                org_id=org_pk
            )
        )
        context['employee_exists'] = (
            self.services.user_organization.check_employee_exist(org_id=org_pk)
        )
        context['filials_exists'] = (
            self.services.organization.get_filials_by_org_id(org_id=org_pk)
        )
        context['departments_exists'] = (
            self.services.organization.check_departments_exists(org_id=org_pk)
        )
        org_tariff_pkg = (
            self.services.org_tariff_package.get_tariff_package_by_org(
                org=context.get('organization')
            )
        )
        context['org_tariff_pkg_is_not_payed'] = (
            self.services.org_tariff_package.check_org_tariff_pkg_payed(
                org_tariff_pkg=org_tariff_pkg
            )
        )
        context['debug'] = settings.DEBUG

        return context


class AbstractListView(LoginRequiredMixin, ListView):
    """
    Abstract class view for all class list views
    """
    services = ServiceClasses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**self.kwargs)
        org_pk = self.kwargs.get('org_pk')
        context['organization'] = (
            self.services.organization
                .get_organization_by_id(org_id=org_pk)
        )
        context['setting'] = (
            self.services.organization_setting
                .get_setting_by_org_id(org_id=org_pk)
        )
        context['employee_exists'] = (
            self.services.user_organization.check_employee_exist(org_id=org_pk)
        )
        context['filials_exists'] = (
            self.services.organization
                .get_filials_by_org_id(org_id=org_pk)
        )
        context['departments_exists'] = (
            self.services.organization
                .check_departments_exists(org_id=org_pk)
        )
        org_tariff_pkg = (
            self.services.org_tariff_package.get_tariff_package_by_org(
                org=context.get('organization')
            )
        )
        context['org_tariff_pkg_is_not_payed'] = (
            self.services.org_tariff_package.check_org_tariff_pkg_payed(
                org_tariff_pkg=org_tariff_pkg
            )
        )
        context['debug'] = settings.DEBUG

        return context


# Main (Class Based Views)
class MainTemplateView(AbstractListView):
    template_name = 'pages/main/main-add-staff.html'
    paginate_by = 5
    context_object_name = 'user_organizations'

    def get_queryset(self):
        return (
            self.services.user_organization.get_user_orgs_by_org(
                org_id=self.kwargs.get('org_pk')
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filials_exists'] = (
            self.services.organization.check_filials_exists(
                org_id=self.kwargs.get('org_pk')
            )
        )
        context['filials'] = (
            self.services.organization.get_organizations(
                org_id=self.kwargs.get('org_pk')
            )
        )
        context['departments'] = (
            self.services.organization.get_sub_organizations(
                org_id=self.kwargs.get('org_pk')
            )
        )

        return context


# Employees (Class Based Views)
class EmployeesListView(AbstractListView):
    template_name = 'pages/employees/employees_list.html'
    paginate_by = 5
    context_object_name = 'user_organizations'

    def get_queryset(self):
        qs = (
            self.services.user_organization.get_user_orgs_by_org(
                org_id=self.kwargs.get('org_pk'),
            )
        )

        return qs


class EmployeesCreateView(AbstractTemplateView):
    template_name = 'pages/employees/employee_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org_setting'] = (
            self.services.organization_setting.get_setting_by_org_id(
                org_id=context.get('org_pk'),
            )
        )
        context['filials'] = (
            self.services.organization.get_filials_by_org_id(
                org_id=context.get('org_pk'),
            )
        )
        context['departments'] = (
            self.services.organization.get_departments_by_org(
                org=context.get('organization'),
            )
        )

        return context

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(data=request.body)
        organization = (
            self.services.organization.get_organization_by_id(
                org_id=data.get('org_id'),
            )
        )
        filial = (
            self.services.organization.get_organization_by_id(
                org_id=data.get('filial_id'),
            )
        )
        department = (
            self.services.organization.get_organization_by_id(
                org_id=data.get('depart_id'),
            )
        )
        user = self.services.user.create_user(data=data)

        if department:
            self.services.user_organization.create_user_organization(
                user=user, organization=department, data=data,
            )

            return JsonResponse({'detail': 'success'}, status=201)

        if filial:
            self.services.user_organization.create_user_organization(
                user=user, organization=filial, data=data
            )

            return JsonResponse({'detail': 'success'}, status=201)

        else:
            self.services.user_organization.create_user_organization(
                user=user, organization=organization, data=data,
            )

            return JsonResponse({'detail': 'success'}, status=201)


class EmployeeEditView(AbstractTemplateView):
    template_name = 'pages/employees/employee_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = context.get('organization')
        context['user_org'] = (
            self.services.user_organization.get_user_org_by_id(
                user_org_id=context.get('user_org_pk'),
            )
        )
        context['filials'] = (
            self.services.organization.get_filials_by_org_id(
                org_id=organization.id,
            )
        )
        context['departments'] = (
            self.services.organization.get_departments_by_org(org=organization)
        )

        return context

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(request.body)
        user_org = (
            self.services.user_organization.get_user_org_by_id(
                user_org_id=data.get('user_org_id'),
            )
        )
        self.services.user_organization.delete_user_organization(user_org)
        success_url = reverse(
            viewname='organizations:employees_list',
            kwargs={'org_pk': data.get('org_pk')},
        )

        return JsonResponse({'success_url': success_url}, status=200)

    def put(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(data=request.body)
        user_org = (
            self.services.user_organization.get_user_org_by_id(
                user_org_id=data.get('user_org_id'),
            )
        )
        self.services.user_organization.update_user_organization(
            user_org=user_org, data=data,
        )
        response = self.services.user.update_user(user=user_org.user, data=data)

        return JsonResponse(response, status=response.get('status_code'))


class EmployeeImportView(AbstractTemplateView):
    template_name = 'pages/employees/employee_import.html'

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        org = self.services.organization.get_organization_by_id(
            org_id=kwargs.get('org_pk')
        )
        response = self.services.user.import_employee_data_to_db(
            file=file, org=org,
        )

        return response


class DownloadEmployeesExcelView(View):
    services = ServiceClasses

    def get(self, request, *args, **kwargs):
        org = self.services.organization.get_organization_by_id(
            org_id=kwargs.get('org_pk'),
        )
        filials = self.services.organization.get_filials_by_org_id(
            org_id=org.id,
        )
        response = self.services.user.generate_import_excel_template(
            org=org, filials=filials,
        )

        return response


# Filials (Class Based Views)
class FilialsListView(AbstractTemplateView):
    template_name = 'pages/filials/filials-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filials'] = (
            self.services.organization.get_filials_by_org_id(
                org_id=kwargs.get('org_pk'),
            )
        )

        return context


class FilialDetailView(AbstractTemplateView):
    template_name = 'pages/filials/filial-detail.html'
    user_table_tmp = 'components/users_table_tmp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filial = self.services.organization.get_organization_by_id(
            org_id=kwargs.get('filial_pk')
        )
        departments = self.services.organization.get_departments_by_user_org(
            filial_pk=kwargs.get('filial_pk')
        )

        context['filial'] = filial
        context['departments'] = departments

        return context

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(request.body)
        department = self.services.organization.get_department_by_user_org(
            department_pk=data.get('depart_pk')
        )
        context = {
            'department': department,
            'is_hide': data.get('is_hide', True),
        }
        html = self.services.organization.get_html_template(
            request=request, tmp_name=self.user_table_tmp, data=context,
        )

        return JsonResponse({'html': html}, status=200)


class FilialCreateView(AbstractTemplateView):
    template_name = 'pages/filials/filial-create.html'

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(request.body)
        org = (
            self.services.organization.get_organization_by_id(
                org_id=data.get('org_id'),
            )
        )
        filial = self.services.organization.create_organization(
            org_name=data.get('filial_name'),
            parent_org=org,
            location=data.get('location', None),
        )
        self.services.organization.create_departments(
            data=data, filial=filial,
        )

        return JsonResponse({'detail': 'success'}, status=201, safe=False)


class FilialAddAdminView(AbstractTemplateView):
    template_name = 'components/search_list_to_add_filial_admin.html'

    def get(self, request, *args, **kwargs):
        user_orgs = (
            self.services.user_organization
                .filter_users_by_request_data(request, **kwargs)
        )

        html = self.services.organization.get_html_template(
            request, tmp_name=self.template_name, data={'user_orgs': user_orgs},
        )

        return JsonResponse({'html': html}, status=200)

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(data=request.body)
        user = self.services.user.get_user_by_id(user_id=data.get('user_id'))
        filial = self.services.organization.get_organization_by_id(
            org_id=data.get('filial_id')
        )
        self.services.organization.set_admin_to_filial(user, filial)

        return JsonResponse({'detail': 'success'}, status=200)


class UserOrgView(AbstractTemplateView):
    user_table_tmp = 'components/users_table_tmp.html'

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(request.body)
        department = self.services.organization.get_department_by_user_org(
            department_pk=data.get('depart_pk'),
        )
        organization = self.services.organization.get_organization_by_id(
            org_id=data.get('org_id')
        )
        context = {
            'department': department,
            'is_hide': data.get('is_hide', True),
            'organization': organization,
        }
        html = self.services.organization.get_html_template(
            request=request, tmp_name=self.user_table_tmp, data=context,
        )

        return JsonResponse({'html': html}, status=200)


# Departments (Class Based Views)
class DepartmentsListView(AbstractTemplateView):
    template_name = 'pages/departments/departments-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = (
            self.services.organization.get_departments_by_org(
                org=context.get('organization'),
            )
        )

        return context


class DepartmentDetailView(AbstractTemplateView):
    template_name = 'pages/departments/department-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.services.organization.get_department_by_user_org(
            department_pk=kwargs.get('depart_pk')
        )
        context['late_agg'] = (
            self.services.worktime.get_user_aggregated_lates(
                department=department,
            )
        )
        context['department'] = department
        print(context)
        return context


class DepartmentCreateView(AbstractTemplateView):
    template_name = 'pages/departments/department-create.html'

    def get_context_data(self, **kwargs):
        context = super(DepartmentCreateView, self).get_context_data(**kwargs)
        context['filials'] = self.services.organization.get_filials_by_org_id(
            org_id=kwargs.get('org_pk')
        )

        return context

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(request.body)
        organization = (
            self.services.organization.get_organization_by_id(
                org_id=data.get('org_id'),
            )
        )
        self.services.organization.create_department(data, organization)

        return JsonResponse({'detail': 'success'}, status=201)


class DepartmentListByFilialView(AbstractTemplateView):
    template_name = 'components/departments_list.html'

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(request.body)

        filial = (
            self.services.organization.get_organization_by_id(
                org_id=data.get('filial_id'),
            )
        )

        departs = (
            self.services.organization.get_departments_by_filial(
                filial=filial,
            )
        )

        html = self.services.organization.get_html_template(
            request, tmp_name=self.template_name, data={'departments': departs},
        )

        return JsonResponse({'html': html}, status=200, safe=False)


# Reports (Class Based Views)
class ReportsListView(AbstractListView):
    template_name = 'pages/reports/reports_list.html'
    paginate_by = 2
    context_object_name = 'departments'

    def get_queryset(self):
        return (
            self.services.organization.get_departments_for_reports(
                org_id=self.kwargs.get('org_pk'),
            )
        )


class ReportDetailView(AbstractListView):
    template_name = 'pages/reports/reports-detail.html'
    paginate_by = 5
    context_object_name = 'work_times'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**self.kwargs)
        user_org = (
            self.services.user_organization.get_user_org_by_id(
                user_org_id=context.get('user_org_id'),
            )
        )
        context['user_org'] = user_org

        return context

    def get_queryset(self):
        qs, _ = (
            self.services.worktime.get_work_times_of_user_org(
                request=self.request,
                user_org_id=self.kwargs.get('user_org_id'),
            )
        )

        return qs


class ReportsDownloadView(View):
    services = ServiceClasses

    def get(self, request, **kwargs):
        departments, start_time, end_time = (
            self.services.organization.get_departments_work_times(
                request=request,
                org_id=kwargs.get('org_pk'),
            )
        )
        response = (
            self.services.worktime.generate_departments_reports(
                departments, start_time, end_time
            )
        )

        return response


class ReportDownloadView(View):
    services = ServiceClasses

    def get(self, request, **kwargs):
        user_org = (
            self.services.user_organization.get_user_org_by_id(
                user_org_id=kwargs.get('user_org_id')
            )
        )
        work_times, agg_late_count = (
            self.services.worktime.get_work_times_of_user_org(
                request=request, user_org_id=user_org.id
            )
        )
        response = (
            self.services.worktime.generate_employee_reports(
                user_org, work_times, agg_late_count,
            )
        )

        return response


class ReportPrintView(View):
    services = ServiceClasses
    template = 'components/report-template.html'

    def get(self, request, **kwargs):
        work_times, _ = self.services.worktime.get_work_times_of_user_org(
            request=request, user_org_id=kwargs.get('user_org_id'),
        )
        user_org = self.services.user_organization.get_user_org_by_id(
            user_org_id=kwargs.get('user_org_id')
        )
        data = {
            'work_times': work_times,
            'user_org': user_org,
        }
        html = self.services.organization.get_html_template(
            request=request, tmp_name=self.template, data=data,
        )

        return JsonResponse({'html': html}, status=200)


# Settings (Class Based Views)
class OrganizationSettingView(AbstractTemplateView):
    template_name = 'pages/settings/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filials'] = (
            self.services.organization.get_filials_by_org_id(
                org_id=context.get('org_pk'),
            )
        )

        return context

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(data=request.body)
        self.services.organization_setting.update_org_setting(data=data)
        employee_exist = (
            self.services.user_organization.check_employee_exist(
                org_id=kwargs.get('org_pk'),
            )
        )
        redirect_url = reverse(
            'organizations:filials_list',
            kwargs={'org_pk': kwargs.get('org_pk')},
        )

        return JsonResponse({
            'employee_exist': employee_exist,
            'redirect_url': redirect_url,
        }, status=200)


class QrCodeDownloadView(View):
    services = ServiceClasses

    def get(self, request, *args, **kwargs):
        org = (
            self.services.organization.get_organization_by_id(
                org_id=request.GET.get('org_pk')
            )
        )
        setting = (
            self.services.organization_setting.get_setting_by_org(org=org)
        )

        return JsonResponse({'qr_code_url': setting.qr_code.url}, status=200)


# Tariffs (Class Based Views)
class TariffTemplateView(AbstractTemplateView):
    template_name = 'pages/tariffs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FeedbackForm()
        context['tariffs'] = self.services.tariff.get_all_tariffs()
        context['current_tariff_package'] = (
            self.services.org_tariff_package.get_tariff_package_by_org(
                org=context.get('organization')
            )
        )

        return context


class TariffPackagesListView(View):
    template_name = 'components/tariffs_modal.html'
    services = ServiceClasses

    def get(self, request, *args, **kwargs):
        tariff = (
            self.services.tariff.get_tariff_by_pk(
                tariff_pk=request.GET.get('tariff_pk')
            )
        )

        if not tariff:
            return JsonResponse({'error': 'тариф не найден'}, status=404)

        packages = (
            self.services.package.get_packages_by_tariff(tariff=tariff)
        )
        data = {'packages': packages, 'tariff': tariff}
        html = (
            self.services.organization.get_html_template(
                request=request, tmp_name=self.template_name, data=data
            )
        )

        return JsonResponse({'html': html}, status=200)


# Global searcher (Class Based View)
class GlobalUserSearchView(AbstractTemplateView):
    template_name = 'components/global_search_result_users_list.html'

    def get(self, request, *args, **kwargs):
        user_orgs = (
            self.services.user_organization.filter_users_by_request_data(
                request=request, **kwargs,
            )
        )

        html = self.services.organization.get_html_template(
            request, tmp_name=self.template_name,
            data={'user_orgs': user_orgs, 'org_id': kwargs.get('org_pk')}
        )

        return JsonResponse({'html': html}, status=200)


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    services = ServiceClasses

    def post(self, request, **kwargs):
        data = self.services.organization.parse_data(request.body)

        self.services.feedback.create_feedback(phone=data.get('phone'))

        return JsonResponse({'detail': 'success'}, status=201)
