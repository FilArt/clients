from rest_framework_nested import routers

from apps.cards.viewsets import CardViewSet, CardAttachmentViewSet

card_router = routers.SimpleRouter()
card_router.register("cards", CardViewSet)
card_router.register("attachments", CardAttachmentViewSet)
