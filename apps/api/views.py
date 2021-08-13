from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.api.models import VersionControl
from apps.api.serializers import (
    UserPhoneNumberSerializer,
    UserOrganizationSerializer,
    UserOrganizationDetailSerializer,
    WorkTimeSerializer,
    VersionControlSerializer,
)
from apps.organizations.models import UserOrganization, WorkTime
from apps.services.fabric import ServiceClasses
from apps.users.constances import POSITIONS
from apps.users.services import UserQueryService


class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserPhoneNumberSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserQueryService.get_user_by_phone_number(
            serializer.data.get('phone_number')
        )

        return Response({'token': user.auth_token.key})


class UserOrganizationListAPIView(ListAPIView):
    serializer_class = UserOrganizationSerializer
    queryset = UserOrganization.objects.all()

    def get_queryset(self):
        qs = super().get_queryset().filter(
            user=self.request.user,
        ).exclude(position=POSITIONS.get('ADMIN'))

        return qs


class UserOrganizationDetailAPIView(RetrieveAPIView):
    serializer_class = UserOrganizationDetailSerializer
    queryset = UserOrganization.objects.all()
    services = ServiceClasses

    def post(self, request, *args, **kwargs):
        user_org = self.services.user_organization.get_user_org_by_id(
            user_org_id=kwargs.get('pk')
        )

        self.services.worktime.create_user_worktime(user_org=user_org)

        return Response(
            data={'detail': _('Посещение создано!')},
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request, *args, **kwargs):
        user_org = self.services.user_organization.get_user_org_by_id(
            user_org_id=kwargs.get('pk')
        )
        worktime = self.services.worktime.get_user_worktime(user_org)
        self.services.worktime.update_user_worktime(worktime)

        return Response(
            data={'detail': _('Время посещения обновлено!')},
            status=status.HTTP_200_OK,
        )


class WorkTimeListAPIView(ListAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    services = ServiceClasses

    def get_queryset(self):
        qr = self.services.worktime.get_work_times(self.request, self.kwargs)

        return qr


class VersionRetrieveView(RetrieveAPIView):
    serializer_class = VersionControlSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return VersionControl.objects.get(pk=1)
