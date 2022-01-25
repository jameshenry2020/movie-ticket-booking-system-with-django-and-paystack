from django import forms
from .models import Audience


GENGER_SELECT=(
    ('M', 'male'),
    ('F', 'female')
)

#form to add audience
class AddAudienceForm(forms.ModelForm):
    class Meta:
        model=Audience 
        fields=['name', 'email', 'gender']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Email'}),
            'gender':forms.Select(attrs={'class':'form-select', 'placeholder':'gender'})
        }
