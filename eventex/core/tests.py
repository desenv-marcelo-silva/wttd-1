from django.test import TestCase

class homeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """Must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html as template"""
        self.assertTemplateUsed(self.response, 'index.html')