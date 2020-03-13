from django import forms 
from box.shop.item.models import * 
from ..models import * 


class ItemForm(forms.ModelForm):
    unit = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"size":"10"}))
    class Meta:
        model = Item 
        exclude = []


class ChangeCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    category = forms.ModelChoiceField(label=("Категорія"),queryset=ItemCategory.objects.all())


class ChangeBrandForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    brand = forms.ModelChoiceField(label=("Бренд"), queryset=ItemBrand.objects.all())


class ChangeMarkersForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    markers = forms.ModelMultipleChoiceField(
        label=("Маркери"),
        queryset=ItemMarker.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )


