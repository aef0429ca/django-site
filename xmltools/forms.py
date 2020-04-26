from django import forms
from xmltools.models import Document



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', 'file_name',)
        widgets = {'file_name': forms.HiddenInput()}

class UrlForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('url', 'file_name',)
        widgets = {'file_name': forms.HiddenInput()}
        

class FormatForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file_name', 'format_guess',)
        widgets = {'file_name': forms.HiddenInput()}
        
        
    
   


