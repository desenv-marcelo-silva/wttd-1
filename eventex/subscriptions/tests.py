from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        #self.assertContains(self.resp, 'type="text"', 3)
        #self.assertContains(self.resp, 'type="email')
        self.assertContains(self.resp, 'type="submit')

    def test_csrf(self):
        """html form must have a csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        self.data = dict(name="Marcelo Silva", cpf="09876543211",
                    email="desenv.marcelo.silva@gmail.com", phone="12 99121-6615")
        self.resp = self.client.post('/inscricao/', self.data)
        self.outbox = mail.outbox[0]

    def test_post(self):
        """Valid post should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = self.outbox
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = self.outbox
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = self.outbox
        expect = ['contato@eventex.com.br', 'desenv.marcelo.silva@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = self.outbox

        self.assertIn('Marcelo Silva', email.body)
        self.assertIn('09876543211', email.body)
        self.assertIn('desenv.marcelo.silva@gmail.com', email.body)
        self.assertIn('12 99121-6615', email.body)


class SubscribeInvalidPost(TestCase):
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

class SubscribeSucessMessage(TestCase):
    def test_message(self):
        data = dict(name="Macelo Silva", cpf="012345678901",
                    email='desenv.marcelo.silva@gmail.com', phone="12 99121-6615")

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')