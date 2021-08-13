from apps.organizations.services import (
    OrganizationQueryService,
    OrganizationSettingQueryService,
    UserOrganizationQueryService,
    WorkTimeQueryService,
    FeedbackQueryService,
)
from apps.payment.services import (
    TariffsQueryServiсe,
    PackageQueryService,
    OrganizationTariffPackageQueryService,
    PaymentService,
    PayboxService,
)
from apps.users.services import UserQueryService


class Services:
    organization = OrganizationQueryService
    user_organization = UserOrganizationQueryService
    organization_setting = OrganizationSettingQueryService
    user = UserQueryService
    worktime = WorkTimeQueryService
    feedback = FeedbackQueryService
    tariff = TariffsQueryServiсe
    package = PackageQueryService
    org_tariff_package = OrganizationTariffPackageQueryService
    payment = PaymentService
    paybox = PayboxService


ServiceClasses = Services()

__all__ = ['ServiceClasses']
