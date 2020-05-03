from django.forms import ModelForm, PasswordInput
from .models import GlobalConfig


class GlobalConfigForm(ModelForm):
    class Meta:
        model = GlobalConfig
        exclude = []
        widgets = {
            "password": PasswordInput(render_value=True),
        }
