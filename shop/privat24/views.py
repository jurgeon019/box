from .integration import Privat24Integration
from .forms import Privat24FrontForm
from django import forms 

class CustomPrivat24Form(Privat24FrontForm):
    amt = forms.CharField(widget=forms.HiddenInput())
    ccy = forms.CharField(widget=forms.HiddenInput())


def pay_privat24(request):
    template = 'pay_privat24.html'
    # order = Order.objects.get(sk=get_sk(request))
    # amt = order.price
    # order_pk = order.pk.
    # details = order.comments
    id = request.session.get('order_id', 1)
    request.session['order_id'] = id
    request.session['order_id'] += id
    print(id)
    amt = '2'
    order_pk = '43'
    details = 'Comment'
    p24 = Privat24Integration({
        "amt": amt,
        "ccy": "UAH",
        "order": order_pk,
        "details":details,
        'form_class': CustomPrivat24Form,
    })
    context = {}
    context['integration'] = p24
    return render(request, template, context)