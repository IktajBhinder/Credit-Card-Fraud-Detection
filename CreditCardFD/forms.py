from django import forms
from django.forms import fields
from  CreditCardFD.models import upload1

class uploadForm(forms.ModelForm):
    class Meta:
        model=upload1
        fields=('file_name','uploadfile','description')