from django import forms 
from box.shop.customer.models import CustomerGroup



class ChangeGroupForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    group = forms.ModelChoiceField(label=("Група"), queryset=CustomerGroup.objects.all())