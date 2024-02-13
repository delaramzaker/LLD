from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Upload File', widget=forms.FileInput(attrs={'class': 'button'}))

class CombinedForm(forms.Form):
    file = forms.FileField(label='Upload File', widget=forms.FileInput(attrs={'class': 'button'}))
    question = forms.CharField(label='Your Question', max_length=255, widget=forms.TextInput(attrs={'class': 'text_field'}))
