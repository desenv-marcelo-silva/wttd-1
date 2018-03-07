from django.core import mail
from django.test import TestCase

class SubscribePostValid(TestCase):
    def setUp(self):
        self.data = dict(name="Marcelo Silva", cpf="09876543211",
                    email="desenv.marcelo.silva@gmail.com", phone="12 99121-6615")
        self.client.post('/inscricao/', self.data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'desenv.marcelo.silva@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Marcelo Silva',
            '09876543211',
            'desenv.marcelo.silva@gmail.com',
            '12 99121-6615'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)