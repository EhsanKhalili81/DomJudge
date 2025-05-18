from django.db import models
from Accounting.models import CustomUser
from Questions.models import Question
# Create your models here.

import os

def user_directory_path(instance, filename):
    username = str(instance.student.username)
    title = str(instance.question.title)
    return os.path.join('Submissions', username, title, filename)

class Submissions(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    solution_file = models.FileField(upload_to=user_directory_path)
    final_result = models.BooleanField(default=False)
    score = models.SmallIntegerField(default=0)
    sent_date = models.DateTimeField(auto_now_add=True)
    is_compiled = models.BooleanField(default=False)
    is_Checked = models.BooleanField(default=False)
    is_contest = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} --> {self.question.title}"
    


class Contest(models.Model):
    title = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
class Contester(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest,on_delete=models.CASCADE)
    penalty = models.IntegerField(default=0)
    score = models.SmallIntegerField(default=0)
    questions = models.JSONField(default={})

class ContestSubmissions(models.Model):
    user = models.ForeignKey(Contester,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)
