import re
from django import forms
from .models import Lead, ContactMethod


class LeadForm(forms.ModelForm):
    # Honeypot — должно быть пустым
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    privacy = forms.BooleanField(required=True, error_messages={
        "required": "Необходимо согласие на обработку персональных данных."
    })

    class Meta:
        model = Lead
        fields = ["name", "phone", "email", "contact_method", "object_type", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["object_type"].required = False
        self.fields["email"].required = False
        self.fields["contact_method"].required = False

    def clean_object_type(self):
        value = self.cleaned_data.get("object_type", "")
        if not value:
            return "other"
        return value

    def clean_contact_method(self):
        value = self.cleaned_data.get("contact_method", "")
        if value not in dict(ContactMethod.choices):
            return ContactMethod.PHONE
        return value

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        digits_only = re.sub(r"[\s\-\(\)]", "", phone)
        if not re.match(r"^\+?[0-9]{7,15}$", digits_only):
            raise forms.ValidationError("Введите корректный номер телефона.")
        return phone

    def clean(self):
        cleaned = super().clean()
        contact_method = cleaned.get("contact_method", ContactMethod.PHONE)
        email = cleaned.get("email", "").strip()
        if contact_method == ContactMethod.EMAIL and not email:
            self.add_error("email", "Укажите email для связи.")
        return cleaned

    def clean_privacy(self):
        value = self.cleaned_data.get("privacy")
        if not value:
            raise forms.ValidationError("Необходимо согласие на обработку данных.")
        return value
