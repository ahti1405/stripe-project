from django.conf import settings
from django.views.generic import TemplateView, DetailView

import stripe

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        })
        return context


class SessionIdAPIView(APIView):
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(id=item_id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return Response({'id': checkout_session.id})


class HtmlPageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            item_id = self.kwargs['pk']
            item = Item.objects.get(id=item_id)
        except:
            return Response({'html-page': 'There is no webpage for this input.'})
        else:
            return Response({'html-page': f'{YOUR_DOMAIN}/{item_id}'})
        
