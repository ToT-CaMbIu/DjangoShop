from django.test import TestCase
from .models import Category

class ProductTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Рвловыа-hjsdf")
        Category.objects.create(name="Что-то")
        check = Category.objects.get(name="Рвловыа-hjsdf")
        check2 = Category.objects.get(name="Что-то")
        check.save()
        check2.save()

    def test_products(self):
        mono = Category.objects.get(name="Рвловыа-hjsdf")
        mono2 = Category.objects.get(name="Что-то")
        self.assertEqual(mono.get_slug(), 'rvlovya-hjsdf')
        self.assertEqual(mono2.get_slug(), 'chto-to')

