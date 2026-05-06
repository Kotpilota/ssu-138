import re
from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    # Honeypot — должно быть пустым
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    privacy = forms.BooleanField(required=True, error_messages={
        "required": "Необходимо согласие на обработку персональных данных."
    })

    class Meta:
        model = Lead
        fields = ["name", "phone", "object_type", "message"]

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not re.match(r"^[\d\+\-\(\)\s]{7,25}$", phone):
            raise forms.ValidationError("Введите корректный номер телефона.")
        return phone

    def clean_privacy(self):
        value = self.cleaned_data.get("privacy")
        if not value:
            raise forms.ValidationError("Необходимо согласие на обработку данных.")
        return value
