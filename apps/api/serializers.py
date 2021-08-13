from django.utils import timezone
from rest_framework import serializers

from apps.api.models import VersionControl
from apps.organizations.models import Organization, UserOrganization, WorkTime
from utils.user_phone_number_regex import phone_regex


class UserPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=15, validators=[phone_regex],
    )


class OrganizationSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    org_id = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('org_id', 'name', "full_name")

    @staticmethod
    def get_full_name(instance):
        if not instance.parent_org:
            return None
        elif instance.parent_org.parent_org is not None:
            return f'{instance.parent_org.parent_org.name} ({instance.name})'
        elif instance.parent_org is not None:
            return f'{instance.parent_org.name} ({instance.name})'
        else:
            return f'{instance.name}'

    @staticmethod
    def get_org_id(instance):
        if instance.is_department:
            return instance.parent_org.id
        if instance.parent_org is None:
            return instance.id
        return instance.parent_org.id


class UserOrganizationSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(required=False)

    class Meta:
        model = UserOrganization
        fields = ('id', 'organization')


class UserOrganizationDetailSerializer(UserOrganizationSerializer):
    organization = OrganizationSerializer(read_only=True)
    user_full_name = serializers.CharField(source="user.get_full_name",
                                           read_only=True)
    work_time = serializers.SerializerMethodField()

    class Meta:
        model = UserOrganization
        fields = (
            'id', 'organization', 'user_full_name', 'work_time',
        )

    @staticmethod
    def get_work_time(instance):

        return WorkTime.objects.filter(
                    user_organization=instance,
                    start_time__day=timezone.datetime.now().day).exists()


class WorkTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkTime
        fields = ('start_time', 'end_time', 'is_late')


class VersionControlSerializer(serializers.ModelSerializer):

    class Meta:
        model = VersionControl
        fields = ('version', 'force_update')
