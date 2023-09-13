from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import *

import os
import re
from django.utils import timezone 



class SignUpForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','username','password1','password2']
        # fields="__all__"
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Firstname"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control","placeholder":"password"}),
            "password2":forms.PasswordInput(attrs={"class":"form-control"}),
        }


class SignInForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))


# CHECK VIDEO FILE EXTENSION AND FILE SIZE
def validate_video_file_extension(value):
    allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise forms.ValidationError("File type is not supported. Please upload a video file in mp4, avi, mov, mkv or wmv format.")
    

def validate_video_file_size(value):
    max_size = 100 * 1024 * 1024  # 100MB
    if value.size > max_size:
        raise forms.ValidationError("File size exceeds the maximum allowed (100MB).")



class ContentModelForm(forms.ModelForm):
    class Meta:
        model=Content
        fields=['title','video']
        widgets={            
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "video":forms.FileInput(attrs={"class":"video-upload"}),
        }
    
    video=forms.FileField(validators=[validate_video_file_extension,validate_video_file_size])


# CHECK VIDEO FILE EXTENSION AND FILE SIZE
def validate_doc_file_extension(value):
    allowed_extensions = ['.pdf', '.docx', '.ppt', '.txt']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise forms.ValidationError("File type is not supported. Please upload a video file in pdf, docx, ppt or txt format.")
    

def validate_doc_file_size(value):
    max_size = 20 * 1024 * 1024  # 100MB
    if value.size > max_size:
        raise forms.ValidationError("File size exceeds the maximum allowed (20MB).")



class DocumentModelForm(forms.ModelForm):
    class Meta:
        model=DocumentFile
        fields=['title','doc']
        widgets={            
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "doc":forms.FileInput(attrs={"class":"form-control"}),
        }
    
    doc=forms.FileField(validators=[validate_doc_file_extension,validate_doc_file_size])


# CHECK DATE
def validate_future_date(value):
    if value < timezone.now().date():
        raise forms.ValidationError("Date must be today or a future date.")

# def validate_future_time(value):
#     current_time = timezone.now().time()
#     if value <= current_time:
#         raise forms.ValidationError("Time must be in the future.")
    
def validate_end_time_after_start_time(form):
    start_time = form.cleaned_data.get('time_start')
    end_time = form.cleaned_data.get('time_end')

    if start_time and end_time and end_time <= start_time:
        raise forms.ValidationError("End time must be after the start time.")



class EventModelForm(forms.ModelForm):

    class Meta:
        model=EventCalender
        fields="__all__"
        widgets={            
            "event_title":forms.TextInput(attrs={"class":"form-control","placeholder":"Event name"}),
            'is_zoom':forms.CheckboxInput(attrs={"class":"form-control"}),
            'youtube_link':forms.URLInput(attrs={"class":"form-control"}),
            "zoom_link":forms.TextInput(attrs={"class":"form-control","placeholder":"link"}),
        }
    def clean(self):
        cleaned_data = super().clean()

        validate_end_time_after_start_time(self)

        is_zoom = cleaned_data.get('is_zoom')
        youtube_link = cleaned_data.get('youtube_link')
        zoom_link = cleaned_data.get('zoom_link')

        if is_zoom:
            if not zoom_link:
                raise forms.ValidationError("Zoom link is required when 'is_zoom' is checked.")
            if youtube_link:
                raise forms.ValidationError("YouTube link should be empty when 'is_zoom' is checked.")
        else:
            if not youtube_link:
                raise forms.ValidationError("YouTube link is required when 'is_zoom' is not checked.")
            if zoom_link:
                raise forms.ValidationError("Zoom link should be empty when 'is_zoom' is not checked.")

        return cleaned_data
    

    date=forms.DateField(validators=[validate_future_date],widget=forms.DateInput(attrs={'class': 'form-control','placeholder': 'MM/DD/YYYY',}))
    time_start=forms.TimeField(widget=forms.TimeInput(attrs={"class":"form-control","placeholder":"HH:MM:SS"}))
    time_end=forms.TimeField(widget=forms.TimeInput(attrs={"class":"form-control","placeholder":"HH:MM:SS"}))



class QuestAnswerModelForm(forms.ModelForm):
    class Meta:
        model=QuestAnswer
        fields=['question']
        widgets={            
            "question":forms.Textarea(attrs={"class":"form-control border-0","placeholder":"New Query...","cols":100,"rows":4,})
        }