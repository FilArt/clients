from rest_framework.routers import SimpleRouter

from .viewsets import CompanyViewSet, PaginatedOfferViewSet, TarifViewSet, OfferViewSet

router = SimpleRouter()
router.register("companies", CompanyViewSet, basename="companies")
router.register("tarifs", TarifViewSet, basename="tarifs")
router.register("offers", OfferViewSet, basename="offers")
router.register("admin_offers", PaginatedOfferViewSet, basename="admin_offers")
