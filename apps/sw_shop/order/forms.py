from django import forms 
from .models import Status, OrderTag


class ChangeStatusForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    status = forms.ModelChoiceField(label=("Статус"), queryset=Status.objects.all())



class ChangeTagsForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    tags = forms.ModelMultipleChoiceField(
        label=("Теги"),
        queryset=OrderTag.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )
