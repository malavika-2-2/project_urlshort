from django import forms
from .models import Link, ALLOWED_CODE

class LinkForm(forms.ModelForm):
    custom_code = forms.CharField(
        required=False,
        max_length=32,
        help_text="Optional: letters, digits, _ or -, 3–32 chars.",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Link
        fields = ["long_url", "custom_code"]
        widgets = {
            "long_url": forms.URLInput(attrs={
                "placeholder": "https://example.com/very/long/path",
                "class": "form-control"
            }),
        }

    def clean_custom_code(self):
        code = self.cleaned_data.get("custom_code", "").strip()
        if code and not ALLOWED_CODE.fullmatch(code):
            raise forms.ValidationError("Use 3–32 chars: letters, digits, _ or -.")
        if code and Link.objects.filter(code=code).exists():
            raise forms.ValidationError("This short code is already taken.")
        return code

    def save(self, commit=True):
        obj = super().save(commit=False)
        custom = self.cleaned_data.get("custom_code")
        if custom:
            obj.code = custom
        if commit:
            obj.save()
        return obj
