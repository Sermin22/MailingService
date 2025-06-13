from django.forms import ModelForm, BooleanField
from mailing.models import Subscriber


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-check-input' if isinstance(field, BooleanField) else 'form-control'
            field.widget.attrs['class'] = css_class


class SubscriberForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Subscriber
        fields = "__all__"
