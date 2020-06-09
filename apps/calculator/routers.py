from rest_framework.routers import SimpleRouter

from .viewsets import CompanyViewSet, TarifViewSet, OfferViewSet

router = SimpleRouter()
router.register('companies', CompanyViewSet, basename='companies')
router.register('tarifs', TarifViewSet, basename='tarifs')
router.register('offers', OfferViewSet, basename='offers')
