from django import forms
from apps.leads.models import Lead, LeadNote


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
