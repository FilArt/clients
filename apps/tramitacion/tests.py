from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.bids.models import Bid
from apps.calculator.models import Company, Offer
from apps.users.models import CustomUser

from .models import Tramitacion


class ClientTramitacionTests(APITestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="client@mail.com")
        company = Company.objects.create()
        offer = Offer.objects.create(uuid=uuid4(), client_type=0, company=company)
        bid = Bid.objects.create(offer=offer, user=self.user)
        self.tramitacion: Tramitacion = Tramitacion.objects.create(bid=bid)

        self.client.force_login(self.user)

    def test_get_tramitacions(self):
        """
        Ensure list view not accesible by client
        """
        url = reverse("tramitacion-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tramitacion(self):
        """
        Ensure detail view accesible by client
        """
        url = reverse("tramitacion-detail", args=[self.tramitacion.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tramitacion(self):
        url = reverse("tramitacion-list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TramitacionTests(ClientTramitacionTests):
    def setUp(self) -> None:
        super().setUp()
        self.support = CustomUser.objects.create(email="support@mail.com", role="support")
        self.client.force_login(self.support)

    def test_get_tramitacions(self):
        """
        Ensure list view not accesible by support
        """
        url = reverse("tramitacion-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tramitacion(self):
        """
        Ensure detail view accesible by support
        """
        url = reverse("tramitacion-detail", args=[self.tramitacion.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tramitacion(self):
        url = reverse("tramitacion-list")
        data = {"bid": self.tramitacion.bid.id}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_tramitacion(self):
        url = reverse("tramitacion-detail", args=[self.tramitacion.id])
        data = {"scoring": True}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tramitacion.refresh_from_db()
        self.assertTrue(self.tramitacion.scoring)
        self.assertFalse(self.tramitacion.success)

    def test_tramitacion_success(self):
        url = reverse("tramitacion-detail", args=[self.tramitacion.id])
        data = {"scoring": True, "doc": True, "call": True}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tramitacion.refresh_from_db()
        self.assertTrue(self.tramitacion.success)

    def test_update_tramitacion_bid(self):
        url = reverse("tramitacion-detail", args=[self.tramitacion.id])
        bid = Bid.objects.create(user=self.user)
        data = {"bid": bid.id}
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
