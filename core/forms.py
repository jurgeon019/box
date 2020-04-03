from django import forms 


class ChangeForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model  = kwargs['initial']['model']
        widget = kwargs['initial']['widget']
        formfield = kwargs['initial']['formfield']
        self.fields['field'] = formfield(
            label=model._meta.verbose_name,
            queryset=model.objects.all(),
            widget=widget,
        )
