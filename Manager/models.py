from django.db import models

from django.contrib.auth.models import AbstractUser

import os
# Create your models here.


class CustomUser(AbstractUser):
    is_teacher=models.BooleanField(default=False)
    is_manager=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)


class Teacher(models.Model):
    profile=models.ImageField(upload_to="profile_images",verbose_name="profile pic upload")
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100,verbose_name="First Name")
    last_name=models.CharField(max_length=100,verbose_name="Last Name")
    options=(
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other")
    )
    gender=models.CharField(max_length=100,choices=options,verbose_name="Gender")
    dob=models.DateField(max_length=100,verbose_name="Date Of Birth")
    phone=models.IntegerField(verbose_name="Mobile No",null=True)
    email=models.CharField(max_length=100,verbose_name="Email",null=True)
    options2=(
        ('SSLC','SSLC'),
        ('Higher Secondary','Higher Secondary'),
        ('Diploma','Diploma'),
        ('Degree','Degree'),
        ('Post Graduate','Post Graduate'),
        ('Doctorate','Doctorate'),
        ('Other','Other')
    )
    qualification=models.CharField(max_length=100,choices=options2,verbose_name="Qualification")
    designation=models.CharField(max_length=200,verbose_name="Designation")
    is_suspend=models.BooleanField(default=False)



class Student(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,default="")
    image=models.ImageField(upload_to="student_profile",null=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    options=(
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other")
    )
    gender=models.CharField(max_length=100,choices=options)
    dob=models.DateField(max_length=100)
    options2=(
        ('SSLC','SSLC'),
        ('Higher Secondary','Higher Secondary'),
        ('Diploma','Diploma'),
        ('Degree','Degree'),
        ('Post Graduate','Post Graduate'),
        ('Other','Other')
    )
    qualification=models.CharField(max_length=100,choices=options2)
    phone_no=models.IntegerField(null=True)


class Course(models.Model):
    course_name=models.CharField(max_length=500)
    options=(
        ('Academic Subjects','Academic Subjects'),
        ('Professional Development','Professional Development'),
        ('Technical and IT','Technical and IT'),
        ('Creative Arts','Creative Arts'),
        ('Language Learning','Language Learning'),
        ('Hobbies and Interests','Hobbies and Interests'),
        ('Certifications and Exams','Certifications and Exams'),
        ('Specialized Training','Specialized Training'),
    )
    course_category=models.CharField(max_length=100,choices=options)
    description=models.CharField(max_length=500)
    poster=models.FileField(upload_to="course_posters",null=True)
    price=models.IntegerField(null=True)
    option2=(
        (3,3),
        (3,6),
        (3,9),
        (3,12),
    )
    duration=models.IntegerField(choices=option2)
    instructor=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    syllabus_pdf = models.FileField(upload_to='syllabus_pdfs')
    status=models.CharField(max_length=100,null=True)
    # student = models.ForeignKey(Student,on_delete=models.CASCADE)







class Tutorial(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    video=models.FileField(upload_to='tutorial_video')
    date_time=models.DateTimeField(auto_now_add=True)


class Note(models.Model):
    tutorial=models.ForeignKey(Tutorial,on_delete=models.CASCADE)
    name=models.TextField(max_length=100)
    note_file=models.FileField(upload_to='note_file')
    date=models.DateField(auto_now_add=True)


class Assignment(models.Model):
    tutorial=models.ForeignKey(Tutorial,on_delete=models.CASCADE)
    topic=models.CharField(max_length=200)
    description=models.CharField(max_length=500)

class AssignmentFile(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    # options=(
    #     ('Pending', 'Pending'),
    #     ('Submitted', 'Submitted'),
    #     ('Accepted', 'Accepted'),
    #     ('Rejected', 'Rejected'),
    # )
    status = models.CharField(max_length=100,default="Pending")
    ass_file=models.FileField(upload_to='assignment_pdf',verbose_name="Upload Assignment File")


class Test(models.Model):
    tutorial=models.ForeignKey(Tutorial,on_delete=models.CASCADE)
    topic=models.CharField(max_length=200)
    description=models.CharField(max_length=500)   
    no_questions=models.IntegerField(null=True)
    is_question=models.BooleanField(default=False)


class Questions(models.Model):
    test=models.ForeignKey(Test,on_delete=models.CASCADE)
    question=models.CharField(max_length=500)
    A=models.CharField(max_length=300)
    B=models.CharField(max_length=300)
    C=models.CharField(max_length=300)
    D=models.CharField(max_length=300)
    options=(
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    answer=models.CharField(max_length=300,choices=options)




class TestMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)    
    mark = models.IntegerField()
    status = models.CharField(max_length=100,default="Pending")



class Content(models.Model):
    title=models.CharField(max_length=300)
    video=models.FileField(upload_to='content_videos')
    datetime=models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # Delete the associated file when the model instance is deleted
        storage, path = self.video.storage, self.video.path
        if os.path.exists(path):
            storage.delete(path)
        super().delete(*args, **kwargs)


class DocumentFile(models.Model):
    title=models.CharField(max_length=300)
    doc=models.FileField(upload_to='doc_files')
    datetime=models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # Delete the associated file when the model instance is deleted
        storage, path = self.doc.storage, self.doc.path
        if os.path.exists(path):
            storage.delete(path)
        super().delete(*args, **kwargs)


class EventCalender(models.Model):
    event_title=models.CharField(max_length=300)
    date=models.DateField()
    time_start=models.TimeField()
    time_end=models.TimeField()
    youtube_link=models.URLField(blank=True)
    is_zoom=models.BooleanField(default=False)
    zoom_link=models.CharField(max_length=100,blank=True)


class QuestAnswer(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    question=models.CharField(max_length=500)
    datetime=models.DateTimeField(auto_now_add=True,null=True)
    is_answer=models.BooleanField(default=False)
    answer=models.CharField(max_length=500,null=True)

