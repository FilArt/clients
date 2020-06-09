from rest_framework_nested import routers

from apps.cards.viewsets import CardViewSet

card_router = routers.SimpleRouter()
card_router.register('', CardViewSet)
