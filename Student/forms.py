from django import forms

from Manager.models import *
from .models import *

from Teacher.forms import validate_image_file_extension
# TEACHER MODEL FORM
class StudentModelForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['image','first_name','last_name','gender','dob','phone_no','qualification']
        widgets={
            "image":forms.FileInput(attrs={"class":"image-upload"}),
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "gender":forms.Select(attrs={"class":"form-control"}),
            "dob":forms.DateInput(attrs={"class":"form-control"}),
            "phone_no":forms.NumberInput(attrs={"class":"form-control"}),
            "qualification":forms.Select(attrs={"class":"form-control"}),
        }
    image=forms.FileField(validators=[validate_image_file_extension])
    
class AssignmentFileForm(forms.ModelForm):
    class Meta:
        model=AssignmentFile
        fields=['ass_file']
        widgets={
            "first_name":forms.FileInput(attrs={"class":"image-upload"}),
        }


class TestAnswerForm(forms.ModelForm):  
    class Meta:
        model=Questions
        fields=['answer']
        widgets={
            "answer":forms.Select(attrs={"class":"form-control"}),
        }
    # answer=forms.ChoiceField(required=True)