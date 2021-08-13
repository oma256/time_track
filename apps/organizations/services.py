""" Class Based Services for current app """
from datetime import timedelta, date, datetime
from io import BytesIO

from django.contrib.gis.geos import Point
from django.db.models import Q, Count, F, DurationField, ExpressionWrapper
from django.db.models.functions import ExtractHour, ExtractMinute
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound, PermissionDenied

import xlsxwriter

from apps.organizations.models import (
    Organization,
    UserOrganization,
    OrganizationSetting,
    WorkTime,
    Feedback,
)
from apps.services.base import BaseQueryService
from apps.users.constances import POSITIONS


class OrganizationQueryService(BaseQueryService):
    model = Organization

    @classmethod
    def create_organization(cls, org_name=None, parent_org=None, admin=None,
                            location=None):
        organization = cls.model.objects.create(name=org_name,
                                                parent_org=parent_org,
                                                admin=admin)
        OrganizationSettingQueryService.create_org_setting(
            organization=organization, location=location
        )

        if organization.org_settings.location is not None:
            cls.create_qr_code(instance=organization)

        return organization

    @classmethod
    def create_departments(cls, data, filial):
        departs_names = data.get('departments_names')

        if not departs_names:
            return

        objs = [
            cls.model(
                name=name,
                parent_org=filial,
                is_department=True,
            ) for name in departs_names
        ]
        cls.model.objects.bulk_create(objs=objs)

    @classmethod
    def create_department(cls, data, organization):
        cls.model.objects.create(name=data.get('depart_name'),
                                 parent_org=organization,
                                 is_department=True)

    @classmethod
    def get_organization_by_id(cls, org_id):
        try:
            return cls.model.objects.get(id=org_id)
        except (cls.model.DoesNotExist, ValueError):
            return None

    @classmethod
    def get_filials_by_org_id(cls, org_id):
        return cls.model.objects.filter(parent_org=org_id, is_department=False)

    @classmethod
    def get_organization_departments(cls, org):
        return cls.model.objects.filter(parent_org=org, is_department=True)

    @classmethod
    def check_filials_exists(cls, org_id):
        return cls.model.objects.filter(
            parent_org=org_id,
            is_department=False,
        ).exists()

    @classmethod
    def get_departments_by_org(cls, org):
        return cls.model.objects.filter(Q(parent_org=org, is_department=True) |
                                        Q(parent_org__parent_org=org))

    @classmethod
    def get_departments_by_filial(cls, filial):
        return cls.model.objects.filter(parent_org=filial)

    @classmethod
    def get_departments_by_user_org(cls, filial_pk):
        departments = cls.model.objects.filter(parent_org_id=filial_pk)
        user_orgs = (
            UserOrganization.objects
                .filter(organization__in=departments)
                .select_related('user')
        )
        all_work_times = WorkTime.objects.filter(
            user_organization__in=user_orgs
        )
        departments = cls.get_mutable_departments(
            departments, user_orgs, all_work_times,
        )

        return departments

    @classmethod
    def get_department_by_user_org(cls, department_pk):
        department = cls.get_organization_by_id(org_id=department_pk)
        user_orgs = (
            UserOrganization.objects
                .filter(organization_id=department_pk)
                .select_related('user')
        )
        all_work_times = (
            WorkTime.objects.filter(user_organization__in=user_orgs)
        )
        departments = cls.get_mutable_departments(
            [department], user_orgs, all_work_times,
        )

        return departments[0]

    @staticmethod
    def get_mutable_departments(departments, user_orgs, all_work_times):
        def inner(value):
            return user_org.id == value.user_organization_id

        def inner_user_orgs(value):
            return department.id == value.organization_id

        for user_org in user_orgs:
            _work_times = list(filter(inner, all_work_times))
            user_org.last_work_time = _work_times[-1] if _work_times else None

        for department in departments:
            department.user_orgs = list(filter(inner_user_orgs, user_orgs))

        return departments

    @classmethod
    def set_admin_to_filial(cls, user, filial):
        cls.model.objects.filter(pk=filial.id).update(admin=user)

    @classmethod
    def check_filials_exists(cls, org_id):
        return cls.model.objects.filter(
            parent_org_id=org_id, is_department=False
        ).exists()

    @classmethod
    def check_departments_exists(cls, org_id):
        return cls.model.objects.filter(
            parent_org_id=org_id, is_department=True
        ).exists()

    @classmethod
    def get_organizations(cls, org_id):
        orgs = cls.model.objects.filter(
            Q(id=org_id) |
            Q(parent_org_id=org_id),
            is_department=False,
        )

        department_list = cls.model.objects.filter(parent_org__in=orgs)
        user_orgs = UserOrganization.objects.filter(
            Q(organization__in=orgs) | Q(organization__in=department_list)
        )
        work_times = WorkTime.objects.filter(user_organization__in=user_orgs)

        def filter_work_times(value):
            return user_org.id == value.user_organization_id

        def filter_departments(value):
            if org.parent_org is not None:
                return org.id == value.parent_org_id
            else:
                return (
                        org.id == value.parent_org_id and
                        value.is_department is True
                )

        def filter_user_orgs(value):
            return department.id == value.organization_id

        for user_org in user_orgs:
            _work_times = list(filter(filter_work_times, work_times))
            user_org.last_work_time = _work_times[-1] if _work_times else None

        for department in department_list:
            _user_orgs = list(filter(filter_user_orgs, user_orgs))
            department.user_orgs = _user_orgs if _user_orgs else None

        for org in orgs:
            _departments = list(filter(filter_departments, department_list))
            org.departments = _departments if _departments else None

        return orgs

    @classmethod
    def get_sub_organizations(cls, org_id):
        departments = cls.model.objects.filter(
            Q(parent_org_id=org_id) |
            Q(parent_org__parent_org_id=org_id),
            is_department=True,
        )
        user_orgs = UserOrganization.objects.filter(
            organization__in=departments
        )
        work_times = WorkTime.objects.filter(user_organization__in=user_orgs)

        def filter_work_times(value):
            return user_org.id == value.user_organization_id

        def filter_user_orgs(value):
            return department.id == value.organization_id

        for user_org in user_orgs:
            _work_times = list(filter(filter_work_times, work_times))
            user_org.last_work_time = _work_times[-1] if _work_times else None

        for department in departments:
            _user_orgs = list(filter(filter_user_orgs, user_orgs))
            department.user_orgs = _user_orgs if _user_orgs else None

        return departments

    @classmethod
    def get_departments_work_times(cls, request, org_id):
        departments = cls.model.objects.filter(
            Q(parent_org_id=org_id) |
            Q(parent_org__parent_org_id=org_id),
            is_department=True,
        )
        filter_params = {'organization__in': departments}
        start_time = request.GET.get('start_time', None)
        end_time = request.GET.get('end_time', None)

        if start_time and end_time:
            filter_params.update(
                {
                    'work_times__start_time__gte': start_time,
                    'work_times__end_time__lte': end_time,
                }
            )
        else:
            filter_params.update(
                {
                    'work_times__start_time__gte': (timezone.now().today()
                                                    - timedelta(30))
                }
            )

        user_orgs = UserOrganization.objects.filter(
            **filter_params
        ).annotate(
            late=Count('id', filter=Q(work_times__is_late=True)),
            on_time=Count('id', filter=Q(work_times__is_late=False)),
        )

        def user_orgs_filter(value):
            return department.id == value.organization_id

        for department in departments:
            _user_org = list(filter(user_orgs_filter, user_orgs))
            department.user_orgs = _user_org

        return departments, start_time, end_time

    @classmethod
    def get_departments_for_reports(cls, org_id):
        departments = cls.model.objects.filter(
            Q(parent_org_id=org_id)
            | Q(parent_org__parent_org_id=org_id),
            is_department=True
        )

        user_orgs = UserOrganization.objects.filter(
            organization__in=departments)

        def filter_user_orgs(value):
            return department.id == value.organization_id

        for department in departments:
            _user_orgs = list(filter(filter_user_orgs, user_orgs))
            department.user_orgs = _user_orgs

        return departments


class OrganizationSettingQueryService(BaseQueryService):
    model = OrganizationSetting

    @classmethod
    def create_org_setting(cls, organization, location=None):
        params = {'organization': organization}

        if location:
            params['location'] = Point(x=location['lng'], y=location['lat'])

        cls.model.objects.create(**params)

    @classmethod
    def update_org_setting(cls, data):
        data = cls.generate_time(data)
        update_prs = dict(
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            non_fined_minute=data.get('non_fined_min'),
        )

        if data.get('location', None):
            update_prs['location'] = Point(
                x=data['location']['lng'],
                y=data['location']['lat'],
            )

        cls.model.objects.filter(id=data.get('setting_id')).update(**update_prs)
        org = OrganizationQueryService.get_organization_by_id(
            data.get('org_id'))
        cls.create_qr_code(org)

    @classmethod
    def get_setting_by_org_id(cls, org_id):
        try:
            org_setting = cls.model.objects.get(organization_id=org_id)

            return org_setting
        except cls.model.DoesNotExist:
            return None

    @classmethod
    def get_setting_by_org(cls, org):
        try:
            if org.is_department:
                return cls.model.objects.get(organization_id=org.parent_org.id)
            return cls.model.objects.get(organization_id=org.id)
        except cls.model.DoesNotExist:
            raise NotFound


class UserOrganizationQueryService(BaseQueryService):
    model = UserOrganization

    @classmethod
    def create_user_organization(cls, user, organization, data=None):
        data = cls.generate_time(data)
        position = data.get('position', POSITIONS.get('ADMIN'))
        org_setting = OrganizationSettingQueryService.get_setting_by_org(
            org=organization
        )

        cls.model.objects.create(
            user=user,
            organization=organization,
            position=position,
            start_time=data.get('start_time', org_setting.start_time),
            end_time=data.get('end_time', org_setting.end_time),
            non_fined_minute=data.get(
                'non_fined_min', org_setting.non_fined_minute
            ),
        )

    @classmethod
    def delete_user_organization(cls, user_org):
        user_org.delete()

    @classmethod
    def update_user_organization(cls, user_org, data):
        data = cls.generate_time(data)

        user_org.position = data.get('position')
        user_org.start_time = data.get('start_time')
        user_org.end_time = data.get('end_time')
        user_org.non_fined_minute = data.get('non_fined_min')
        user_org.save(update_fields=[
            'position', 'start_time', 'end_time', 'non_fined_minute',
        ])

    @classmethod
    def filter_users_by_request_data(cls, request, **kwargs):
        name = request.GET.get('name')
        org_id = kwargs.get('org_pk')
        user_args = [
            Q(user__first_name__icontains=name)
            | Q(user__last_name__icontains=name)
            | Q(user__middle_name__icontains=name)
        ]
        org_filter_args = [
            Q(organization_id=org_id)
            | Q(organization__parent_org_id=org_id)
            | Q(organization__parent_org__parent_org_id=org_id)
        ]
        users = cls.model.objects.filter(
            *org_filter_args, *user_args
        ).distinct('user_id')

        return users

    @classmethod
    def get_user_org_by_id(cls, user_org_id):
        try:
            return cls.model.objects.get(id=user_org_id)
        except cls.model.DoesNotExist:
            raise NotFound(detail=_('User organization not found'))

    @classmethod
    def get_org_by_parent_org(cls, org):
        return cls.model.objects.filter(
            organization__parent_org=org
        ).distinct('organization')

    @classmethod
    def get_users_by_org_id(cls, org_id):
        return cls.model.objects.filter(
            Q(organization_id=org_id)
            | Q(organization__parent_org_id=org_id)
            | Q(organization__parent_org__parent_org_id=org_id),
            organization__admin=None
        )

    @classmethod
    def get_user_orgs_by_department(cls, department):
        return cls.model.objects.filter(organization=department)

    @classmethod
    def get_user_orgs_by_org(cls, org_id):
        def inner(value):
            return user_org.id == value.user_organization_id

        user_orgs = cls.model.objects.filter(
            Q(organization_id=org_id)
            | Q(organization__parent_org_id=org_id)
            | Q(organization__parent_org__parent_org_id=org_id),
        ).exclude(position__contains=POSITIONS.get('ADMIN'))

        all_work_times = (
            WorkTime.objects.filter(user_organization__in=user_orgs)
        )

        for user_org in user_orgs:
            _work_times = list(filter(inner, all_work_times))
            user_org.last_work_time = _work_times[-1] if _work_times else None

        return user_orgs

    @classmethod
    def check_employee_exist(cls, org_id):
        return cls.model.objects.filter(
            Q(organization_id=org_id) |
            Q(organization__parent_org_id=org_id) |
            Q(organization__parent_org__parent_org_id=org_id)
        ).exclude(
            position__contains=POSITIONS.get('ADMIN')
        ).exists()


class WorkTimeQueryService(BaseQueryService):
    model = WorkTime

    @staticmethod
    def _datetime_filter_kw():
        _tz = timezone.now()

        return {
            'start_time__day': _tz.day,
            'start_time__year': _tz.year,
            'start_time__month': _tz.month,
        }

    @classmethod
    def get_user_worktime(cls, user_org):
        worktime = cls.model.objects.filter(
            user_organization=user_org,
            **cls._datetime_filter_kw(),
        ).first()

        if not worktime:
            raise NotFound

        return worktime

    @classmethod
    def create_user_worktime(cls, user_org):
        is_late = cls._check_employee_is_late(user_org=user_org)
        obj, created = cls.model.objects.get_or_create(
            user_organization=user_org,
            **cls._datetime_filter_kw(),
            defaults={
                'start_time': timezone.now(),
                'is_late': is_late,
            },
        )

        if not created:
            raise PermissionDenied(_('Начало времени уже создано!'))

        cls._set_user_is_checked_status(user_org=user_org)

    @classmethod
    def _check_employee_is_late(cls, user_org):
        _arrived_time = (
            datetime.combine(date.today(), user_org.start_time) +
            timedelta(minutes=user_org.non_fined_minute + 1)
        ).time()

        return cls.convert_to_localtime(timezone.now()).time() >= _arrived_time

    @classmethod
    def _set_user_is_checked_status(cls, user_org):
        user_org.is_checked = not user_org.is_checked
        user_org.save(update_fields=['is_checked'])

    @classmethod
    def update_user_worktime(cls, worktime):

        if worktime.end_time is not None:
            raise PermissionDenied(_('Вы уже отсканировали два раза в день!'))

        cls.model.objects.filter(
            user_organization=worktime.user_organization,
            **cls._datetime_filter_kw(),
        ).update(end_time=timezone.now())

        cls._set_user_is_checked_status(user_org=worktime.user_organization)

    @classmethod
    def get_work_times(cls, request, kwargs):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if date_from is None or date_to is None:
            month_ago_date, current_date = cls.get_last_month_date_range()

            return cls.model.objects.filter(
                user_organization_id=kwargs.get('pk'),
                start_time__range=[month_ago_date, current_date]
            )

        return cls._filter_work_time_by_date_range(kwargs, date_from, date_to)

    @classmethod
    def _filter_work_time_by_date_range(cls, kwargs, date_from, date_to):

        return cls.model.objects.filter(
            user_organization_id=kwargs.get('pk'),
            start_time__range=[
                date_from,
                cls.convert_str_to_date_format(date_to) + timedelta(days=1)
            ]
        )

    @classmethod
    def get_user_aggregated_lates(cls, department):
        month_ago_date, current_date = cls.get_last_month_date_range()

        return cls.model.objects.filter(
            user_organization__organization=department,
            start_time__range=[month_ago_date, current_date],
        ).aggregate(
            late=Count('id', filter=Q(is_late=True)),
            not_late=Count('id', filter=Q(is_late=False)),
        )

    @classmethod
    def get_work_times_of_user_org(cls, request, user_org_id):
        filter_params = {'user_organization_id': user_org_id}
        start_time = request.GET.get('start_time', None)
        end_time = request.GET.get('end_time', None)

        if start_time and end_time:
            filter_params.update(
                {
                    'start_time__gte': start_time,
                    'end_time__lte': end_time,
                }
            )
        else:
            filter_params.update(
                {
                    'start_time__gte': timezone.now().today() - timedelta(30)
                }
            )
        _qs = cls.model.objects.filter(
            **filter_params
        ).order_by(
            'start_time'
        ).annotate(
            hour_duration=ExtractHour(
                ExpressionWrapper(
                    (F('end_time') - F('start_time')),
                    output_field=DurationField()
                )
            ),
            minute_duration=ExtractMinute(
                ExpressionWrapper(
                    (F('end_time') - F('start_time')),
                    output_field=DurationField()
                )
            ),
        )
        agg_late_count = _qs.aggregate(
            late=Count('id', filter=Q(is_late=True)),
            on_time=Count('id', filter=Q(is_late=False)),
        )

        return _qs, agg_late_count

    @classmethod
    def generate_employee_reports(cls, user_org, work_times, agg_late_count):
        output = BytesIO()

        with xlsxwriter.Workbook(output) as workbook:
            worksheet = workbook.add_worksheet('report')
            bold = workbook.add_format({'bold': True, 'border': 1})
            border = workbook.add_format({'border': 1})
            columns = ['Дата', 'Время прихода', 'Время ухода', 'Кол-во часов']

            worksheet.write(0, 0, 'Отчет', bold)
            try:
                worksheet.write(
                    0, 1,
                    f'С {work_times.first().start_time.strftime("%d.%m.%Y")} '
                    f'По {work_times.last().end_time.strftime("%d.%m.%Y")}',
                    border
                )
            except AttributeError:
                worksheet.write(0, 1, '-/-')
            worksheet.write(1, 0, 'Ф.И.О.', bold)
            worksheet.write(1, 1, user_org.user.get_full_name, border)
            worksheet.write(2, 0, 'Должность', bold)
            worksheet.write(2, 1, user_org.position, border)

            if user_org.organization.is_department:
                worksheet.write(3, 0, 'Филиал', bold)
                worksheet.write(
                    3, 1, user_org.organization.parent_org.name, border
                )
                worksheet.write(4, 0, 'Отдел', bold)
                worksheet.write(4, 1, user_org.organization.name, border)
                worksheet.write(5, 0, 'Опозданий', bold)
                worksheet.write(5, 1, agg_late_count.get('late'), border)
                worksheet.write(6, 0, 'Во время', bold)
                worksheet.write(6, 1, agg_late_count.get('on_time'), border)
            else:
                worksheet.write(3, 0, 'Филиал', bold)
                worksheet.write(3, 1, user_org.organization.name, border)
                worksheet.write(4, 0, 'Опозданий', bold)
                worksheet.write(4, 1, agg_late_count.get('late'), border)
                worksheet.write(5, 0, 'Во время', bold)
                worksheet.write(5, 1, agg_late_count.get('on_time'), border)

            for index, item in enumerate(columns, start=3):
                worksheet.write(0, index, item, bold)

            for index, item in enumerate(work_times, start=1):
                worksheet.write(
                    index, 3,
                    cls.convert_to_localtime(
                        item.start_time
                    ).strftime('%d.%m.%Y'),
                    border,
                )
                worksheet.write(
                    index, 4,
                    cls.convert_to_localtime(item.start_time).strftime('%H:%M'),
                    border,
                )
                try:
                    worksheet.write(
                        index, 5,
                        cls.convert_to_localtime(
                            item.end_time
                        ).strftime('%H:%M'),
                        border,
                    )
                except AttributeError:
                    worksheet.write(index, 5, '-/-', border)

                if item.hour_duration is None:
                    worksheet.write(index, 6, '-/-', border)
                else:
                    worksheet.write(
                        index, 6,
                        f'{item.hour_duration} ч.  {item.minute_duration} мин.',
                        border,
                    ),

        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-office'
                         'document.spreadsheetml.sheet'
        )

    @classmethod
    def generate_departments_reports(cls, departments, start_time, end_time):
        output = BytesIO()
        month_ago_date, current_date = cls.get_last_month_date_range()

        if not start_time and not end_time:
            duration_time = f'С {month_ago_date} По {current_date}'
        else:
            duration_time = f'С {start_time} По {end_time}'

        with xlsxwriter.Workbook(output) as workbook:
            worksheet = workbook.add_worksheet('report')
            bold = workbook.add_format({'bold': True, 'border': 1})
            border = workbook.add_format({'border': 1})

            worksheet.write(2, 1, 'Отчет', bold)
            worksheet.write(2, 2, duration_time, border)
            dep_index = 4
            for i, department in enumerate(departments):

                if i:
                    dep_index += 7

                worksheet.write(dep_index, 1, department.name, bold)

                worksheet.write(dep_index + 2, 1, 'Ф.И.О.', bold)
                worksheet.write(dep_index + 2, 2, 'Должность', bold)
                worksheet.write(dep_index + 2, 3, 'Вовремя', bold)
                worksheet.write(dep_index + 2, 4, 'Опоздал', bold)

                for user_org in department.user_orgs:
                    worksheet.write(
                        dep_index + 3, 1,
                        user_org.user.get_full_name,
                        border,
                    )
                    worksheet.write(
                        dep_index + 3, 2,
                        user_org.position,
                        border,
                    )
                    worksheet.write(
                        dep_index + 3, 3,
                        user_org.on_time,
                        border,
                    )
                    worksheet.write(
                        dep_index + 3, 4,
                        user_org.late,
                        border,
                    )

                    dep_index += 1

        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-office'
                         'document.spreadsheetml.sheet'
        )


class FeedbackQueryService:
    model = Feedback

    @classmethod
    def create_feedback(cls, phone):
        cls.model.objects.create(phone=phone)
