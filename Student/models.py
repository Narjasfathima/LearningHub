from django.db import models

from datetime import datetime, timedelta

from Manager.models import *
# Create your models here.
class CoursePurchase(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    date_of_join=models.DateField(auto_now_add=True)
    date_of_end=models.DateField(null=True)
    is_paid=models.BooleanField(default=False)


class Room(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    name=models.CharField(max_length=500)
    slug=models.SlugField(unique=True)
    date_of_end=models.DateField(null=True)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)