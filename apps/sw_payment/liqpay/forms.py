from django import forms 
from .models import LiqpayTransaction


class LiqpayTransactionForm(forms.ModelForm):
  class Meta:
      model = LiqpayTransaction
      exclude = [
        'timestamp',
      ]
