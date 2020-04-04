from django.forms import ModelForm, PasswordInput
from .models import NotificationConfig


class NotificationConfigForm(ModelForm):
    class Meta:
        model = NotificationConfig
        exclude = []
        widgets = {
            "password": PasswordInput(render_value=True),
        }
