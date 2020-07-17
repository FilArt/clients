from rest_framework.routers import SimpleRouter

from . import viewsets

user_router: SimpleRouter = SimpleRouter()
user_router.register("register_user", viewsets.RegisterViewSet)
user_router.register("account", viewsets.AccountViewSet)
user_router.register("users", viewsets.UserViewSet)
user_router.register("leeds", viewsets.LeedsViewSet)
user_router.register("puntos", viewsets.PuntoViewSet)
user_router.register("phones", viewsets.PhoneViewSet)
user_router.register("attachments", viewsets.AttachmentsViewSet)
user_router.register("calls", viewsets.CallViewSet)
