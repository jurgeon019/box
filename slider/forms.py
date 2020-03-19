from .models import Slider 
from django import forms 



class ChangeSliderForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    slider = forms.ModelChoiceField(label=("Слайдер"),queryset=Slider.objects.all())



