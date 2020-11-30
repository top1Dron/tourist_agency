from .service import create_order
from django.test import TestCase

def test_always_true():
    assert True


class CreateOrderTestCase(TestCase):
    def setUp(self):
        self.tour_id = '68'
        self.tour_hotel_id = '1'
        self.client_name = 'Іванов Іван Іванович'
        self.client_phone = '+38(093)1350239'

    def test_create_order(self):
        self.assertTrue(create_order(
            self.tour_id,
            self.tour_hotel_id,
            self.client_name,
            self.client_phone )
        )