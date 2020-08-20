from rest_framework.routers import SimpleRouter

from . import viewsets

user_router: SimpleRouter = SimpleRouter()
user_router.register("register_user", viewsets.RegisterViewSet)
user_router.register("contract_online", viewsets.ContractOnlineViewSet)
user_router.register("contract_online_plus", viewsets.AdditionalContractOnlineViewSet)
user_router.register("contract_online_with_factura", viewsets.WithFacturaContractOnlineViewSet)
user_router.register("fast_contract", viewsets.FastContractViewSet)
user_router.register("account", viewsets.AccountViewSet)
user_router.register("users", viewsets.UserViewSet)
user_router.register("manage_users", viewsets.ManageUsersViewSet)
user_router.register("puntos", viewsets.PuntoViewSet)
user_router.register("phones", viewsets.PhoneViewSet)
user_router.register("attachments", viewsets.AttachmentsViewSet)
user_router.register("calls", viewsets.CallViewSet)
user_router.register("logs", viewsets.RequestLogViewSet)
