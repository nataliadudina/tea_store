from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from .models import TeaCategory, TeaProduct


class GetPagesTestCase(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        """Initialization before executing each test"""

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)    # simulates various requests to the server from the browser
                                            # and gets the result of the server response
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_redirect_write_article(self):
        path = reverse('store_blog:create')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_catalog_data(self):
        # Gets data from db with IN_STOCK status
        data = TeaProduct.stock_objects.all()

        # Gets data from view
        path = reverse('types', kwargs={'type_slug': 'black-tea'})
        response = self.client.get(path)

        # Checks if the list of products on the page is correct
        self.assertQuerysetEqual(response.context_data['object_list'], data[:4], ordered=False)

    def test_category_data(self):
        # Gets data from db
        data = TeaCategory.objects.all()

        # Gets data from view
        path = reverse('catalog')
        response = self.client.get(path)

        # Checks that for each category from data, there is a corresponding product in response.context['object_list']
        for category in data:
            product_exists = any(product.category == category for product in response.context['object_list'])
            self.assertTrue(product_exists, f"No product found for category: {category}")

    def tearDown(self):
        """Actions after completing each test"""
