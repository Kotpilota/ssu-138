from django import forms
from apps.leads.models import Lead, LeadNote
from apps.content.models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            "phone", "email", "address",
            "legal_name", "inn", "ogrn", "address_legal",
            "site_url", "og_image", "map_embed_url",
        ]
        widgets = {
            "address_legal": forms.TextInput(),
            "map_embed_url": forms.TextInput(
                attrs={"placeholder": "https://yandex.ru/map-widget/v1/..."}
            ),
        }


class LeadStatusForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["status"]


class LeadNoteForm(forms.ModelForm):
    class Meta:
        model = LeadNote
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Внутренний комментарий..."})
        }
