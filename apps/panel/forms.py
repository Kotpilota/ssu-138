from django import forms
from apps.leads.models import Lead, LeadNote
from apps.content.models import SiteSettings, Page, Section, SectionItem


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


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            "title", "slug", "is_published",
            "meta_title", "meta_description", "meta_keywords",
            "og_title", "og_description", "og_image",
        ]
        widgets = {
            "meta_description": forms.Textarea(attrs={"rows": 2}),
            "meta_keywords": forms.Textarea(attrs={"rows": 2}),
            "og_description": forms.Textarea(attrs={"rows": 2}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = [
            "block_type", "is_visible", "eyebrow", "title",
            "subtitle", "body", "image", "anchor", "order", "extra",
        ]
        widgets = {
            "subtitle": forms.Textarea(attrs={"rows": 3}),
            "body": forms.Textarea(attrs={"rows": 6}),
            "extra": forms.Textarea(attrs={"rows": 3, "class": "code-field"}),
        }
        help_texts = {
            "extra": "Доп. параметры в формате JSON (обычно не нужно менять).",
            "body": "Для блока «Произвольный HTML» — сюда вставляется HTML.",
        }


class SectionCreateForm(forms.ModelForm):
    """Быстрое создание секции — выбираем только тип, остальное правим потом."""
    class Meta:
        model = Section
        fields = ["block_type"]


SectionItemFormSet = forms.inlineformset_factory(
    Section, SectionItem,
    fields=[
        "order", "number", "title", "subtitle",
        "description", "image", "tag", "link_text", "link_url", "extra",
    ],
    widgets={
        "description": forms.Textarea(attrs={"rows": 2}),
        "extra": forms.Textarea(attrs={"rows": 2, "class": "code-field"}),
    },
    extra=1, can_delete=True,
)


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
