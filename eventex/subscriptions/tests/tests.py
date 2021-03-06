from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """ Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ Must use subscriptions/subscription_form1.html"""
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_form.html")

    def test_html(self):
        """ Html must contain input tags"""
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email', 1),
            ('type="submit', 1),
        )
        for content, qtde in tags:
            with self.subTest():
                self.assertContains(self.resp, content, qtde)

    def test_csrf(self):
        """html form must have a csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)



class SubscribePostValid(TestCase):
    def setUp(self):
        self.data = dict(name="Marcelo Silva", cpf="09876543211",
                    email="desenv.marcelo.silva@gmail.com", phone="12 99121-6615")
        self.resp = self.client.post('/inscricao/', self.data)

    def test_post(self):
        """Valid post should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscriptions(self):
        self.assertTrue(Subscription.objects.exists())

class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid post should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscriptions(self):
        self.assertFalse(Subscription.objects.exists())


class SubscribeSucessMessage(TestCase):
    def test_message(self):
        data = dict(name="Macelo Silva", cpf="012345678901",
                    email='desenv.marcelo.silva@gmail.com', phone="12 99121-6615")

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')