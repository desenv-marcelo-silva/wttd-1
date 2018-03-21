from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name="Marcelo Silva",
            cpf="12345678901",
            email="desenv_marcelo_silva@mail.com",
            phone="12-8211-6615"
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attribute"""
        self.assertIsInstance(self.obj.created_at, datetime)