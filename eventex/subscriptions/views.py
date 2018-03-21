from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)

        if form.is_valid():

            # context = dict(name="Marcelo Silva", cpf="09876543211",
            #             email="desenv.marcelo.silva@gmail.com", phone="12 99121-6615")
            #
            # body = render_to_string('subscriptions/subscription_email.txt',
            #                         context)

            body = render_to_string('subscriptions/subscription_email.txt',
                                    form.cleaned_data)

            mail.send_mail('Confirmação de inscrição',
                           body,
                           'contato@eventex.com.br',
                           ['contato@eventex.com.br', form.cleaned_data['email']])

            Subscription.objects.create(**form.cleaned_data)

            messages.success(request, 'Inscrição realizada com sucesso!')

            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html',
                          {'form': form})
    else:
        context = {'form': SubscriptionForm()}
        return render(request, "subscriptions/subscription_form.html", context)