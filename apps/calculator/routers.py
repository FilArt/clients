from rest_framework.routers import SimpleRouter

from . import viewsets

router = SimpleRouter()
router.register("companies", viewsets.CompanyViewSet, basename="companies")
router.register("tarifs", viewsets.TarifViewSet, basename="tarifs")
router.register("offers", viewsets.OfferViewSet, basename="offers")
router.register("admin_offers", viewsets.PaginatedOfferViewSet, basename="admin_offers")
router.register("priority_offers", viewsets.PriorityOfferViewSet, basename="priority_offers")
router.register("settings", viewsets.CalculatorSettingsViewset, basename="settings")
