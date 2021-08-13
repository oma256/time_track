from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.services.fabric import ServiceClasses


class PaymentCreateView(LoginRequiredMixin, View):
    services = ServiceClasses

    def post(self, request, *args, **kwargs):
        data = self.services.organization.parse_data(request.body)
        org = (
            self.services.organization.get_organization_by_id(
                org_id=data.get('org_id'),
            )
        )
        package = (
            self.services.package.get_package_by_id(
                tariff_pkg_id=data.get('tariff_pkg_id'),
            )
        )

        if package is None:
            return JsonResponse({'error': 'package not found'}, status=404)

        org_tariff_pkg = (
            self.services.org_tariff_package.get_tariff_package_by_org(org=org)
        )
        payment = (
            self.services.payment.create_payment(
                org_tariff=org_tariff_pkg, tariff=package,
            )
        )
        payment_url = self.services.paybox.generate_paybox_url(
            payment=payment, org_id=data.get('org_id'),
        )

        return JsonResponse({'paybox_payment_url': payment_url}, status=200)


class PayboxResultAPIView(View):
    services = ServiceClasses

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        paybox_result = int(request.POST.get('pg_result'))
        pg_order_id = request.POST.get('pg_order_id')

        if paybox_result:
            self.services.payment.update_payment_result(
                request=request, pg_order_id=pg_order_id
            )
            self.services.org_tariff_package.update_current_org_tariff_pkg(
                payment_id=pg_order_id
            )

            return JsonResponse({'detail': 'success'}, status=200)

        return JsonResponse({'error': 'payment required'}, status=402)
