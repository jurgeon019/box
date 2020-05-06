from rest_framework.decorators import api_view
from rest_framework.response import Response 
from datetime import date, datetime
import requests 
from .models import * 
from .serializers import * 





def parse_currencies(pb_date=date.today().strftime('%d.%m.%Y')):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={pb_date}'
    response = requests.get(url).json()
    rates = response.get('exchangeRate', [])
    for rate in rates:
        print(rate)
        sale_rate = rate['saleRateNB']
        purchase_rate = rate['purchaseRateNB']
        # if sale_rate != purchase_rate:
        #     print(rate)
        if 'currency' in rate:
            currency, _ = Currency.objects.get_or_create(code=rate['currency'])
            currency.sale_rate = sale_rate
            currency.purchase_rate = purchase_rate
            if rate['baseCurrency'] == rate['currency']:
                currency.is_main = True 
            currency.save()


@api_view(['GET','POST'])
def currencies(request):
    return Response(CurrencySerializer(Currency.objects.all(), many=True).data)


@api_view(['GET','POST'])
def create_currencies(request):
    parse_currencies()
    return Response({"status":"ok"})

