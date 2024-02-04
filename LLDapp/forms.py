from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
class QuestionForm(forms.Form):
    question = forms.CharField(label='Your Question', max_length=255)


class CombinedForm(forms.Form):
    file = forms.FileField(label='Upload File')
    question = forms.CharField(label='Your Question', max_length=255)

