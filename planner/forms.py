from django import forms

from .models import ActivityType, Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["name", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = ActivityType
        fields = ["name", "color", "description"]
        widgets = {
            "color": forms.TextInput(attrs={"type": "color"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
