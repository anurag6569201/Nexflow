# forms.py
from django import forms
from .models import UserProfileREADME

class READMEForm(forms.ModelForm):
    class Meta:
        model = UserProfileREADME
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
        }
