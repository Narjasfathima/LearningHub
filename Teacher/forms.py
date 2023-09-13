from django import forms

from django.forms import modelformset_factory

from Manager.models import *

from Manager.forms import validate_video_file_extension,validate_video_file_size,validate_doc_file_extension


# TEACHER MODEL FORM
class TeacherModelForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=['profile','first_name','last_name','gender','dob','phone','email','qualification','designation']
        widgets={
            "profile":forms.FileInput(attrs={"class":"image-upload"}),
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "gender":forms.Select(attrs={"class":"form-control"}),
            "dob":forms.DateInput(attrs={"class":"form-control"}),
            "phone":forms.NumberInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "qualification":forms.Select(attrs={"class":"form-control"}),
            "designation":forms.TextInput(attrs={"class":"form-control"}),
        }


def validate_doc_file_extension_teacher(value):
    allowed_extensions = ['.pdf']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise forms.ValidationError("File type is not supported. Please upload a syllabus in pdf format.")
    
def validate_image_file_extension(value):
    allowed_extensions = ['.jpg', '.png']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise forms.ValidationError("File type is not supported. Please upload a image file in jpg or png format.")

class CourseModelForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=['course_name','course_category','description','poster','duration','syllabus_pdf']
        widgets={
            "course_name":forms.TextInput(attrs={"class":"form-control"}),
            "course_category":forms.Select(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "poster":forms.FileInput(attrs={"class":"form-control"}),            
            # "price":forms.NumberInput(attrs={"class":"form-control"}),
            "duration":forms.Select(attrs={"class":"form-control"}),
            "syllabus_pdf":forms.FileInput(attrs={"class":"form-control"}),
        }

    syllabus_pdf=forms.FileField(validators=[validate_doc_file_extension_teacher])
    poster=forms.FileField(validators=[validate_image_file_extension])


class ConfirmAddCourseForm(forms.Form):
    confirm_download = forms.BooleanField(
        required=False,  # The checkbox is optional
        label="Do you want to download the course template?   ",
        widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox-input'}),
    )


class TutorialForm(forms.ModelForm):
    class Meta:
        model=Tutorial
        fields=['title','video']
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "video":forms.FileInput(attrs={"class":"form-control-file border"}),
        }

    video=forms.FileField(validators=[validate_video_file_extension,validate_video_file_size])


class AssignmentModelForm(forms.ModelForm):
    class Meta:
        model=Assignment
        fields=['topic','description']
        widgets={
            "topic":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
        }


class NoteModelForm(forms.ModelForm):
    class Meta:
        model=Note
        fields=['name','note_file']
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "note_file":forms.FileInput(attrs={"class":"form-control"}),
        }
    
    note_file=forms.FileField(validators=[validate_doc_file_extension])



def validate_no_questions(value):
    if value>10 or value < 5:
        raise forms.ValidationError("Minimum no.of questions is 5 and Maximum is 10..")
    


class TestModelForm(forms.ModelForm):
    class Meta:
        model=Test
        fields=['topic','description','no_questions']
        widgets={
            "topic":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "no_questions":forms.NumberInput(attrs={"class":"form-control"}),
        }
    
    
    no_questions=forms.IntegerField(validators=[validate_no_questions])


class TestForm(forms.ModelForm):
    class Meta:
        model=Test
        fields=['topic','description']
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
        }
    



class QuestionsModelForm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=['question','A','B','C','D','answer']
        widgets={
            "question":forms.Textarea(attrs={"class":"form-control"}),
            "A":forms.TextInput(attrs={"class":"form-control","placeholder":"option A"}),
            "B":forms.TextInput(attrs={"class":"form-control","placeholder":"option A"}),
            "C":forms.TextInput(attrs={"class":"form-control","placeholder":"option A"}),
            "D":forms.TextInput(attrs={"class":"form-control","placeholder":"option A"}),
            "answer":forms.Select(attrs={"class":"form-control","placeholder":"option A"}),
        }


class QaAnswerModelForm(forms.ModelForm):
        class Meta:
            model=QuestAnswer
            fields=['question','answer']
            widgets={            
                "question":forms.Textarea(attrs={"class":"form-control border-0","cols":100,"rows":4,}),
                "answer":forms.Textarea(attrs={"class":"form-control border-0","cols":100,"rows":4,})
            }
