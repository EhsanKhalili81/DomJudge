from django.db import models
from Accounting.models import CustomUser
# Create your models here.

class Course(models.Model):
    MAJOR_CHOICES = (
        ('907', '907'),
        ('705', '705'),
        ('302', '302'),
        ('401', '401'),
    )
    title = models.CharField(max_length=30,blank=False)
    teacher = models.ForeignKey(CustomUser,models.CASCADE)
    course_code = models.SmallIntegerField()
    major_code = models.CharField(max_length=20,choices=MAJOR_CHOICES)

    def __str__(self):
        return self.title
    



import os

def user_directory_path(instance, filename):
    username = str(instance.creator.username)
    title = str(instance.title)
    return os.path.join('questions', username, title, filename)
class Question(models.Model):
    LANGUAGE_CHOICES = (
        ('python', 'python'),
        ('c#', 'c#'),
        ('java', 'java'),
    )
    creator = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    title = models.CharField(max_length=50,blank=False)
    description = models.TextField(blank=False)
    input_form = models.TextField()
    output_form = models.TextField()
    question_file = models.FileField(upload_to=user_directory_path,blank=True)
    timelimit = models.SmallIntegerField()
    inputs_file = models.FileField(upload_to=user_directory_path)
    outputs_file = models.FileField(upload_to=user_directory_path)
    language = models.CharField(max_length=10,choices=LANGUAGE_CHOICES,blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    score = models.FloatField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    allowed_number = models.SmallIntegerField()


    def __str__(self):
        return self.title