from django.contrib.admin.decorators import register
from django.db import models
from django.db.models.deletion import CASCADE
import time

from django.db.models.fields.related import OneToOneField

# Create your models here.
class QuestionAnswer(models.Model):
    category = models.CharField(max_length=100)
    question=models.CharField(max_length=300)
    answer=models.CharField(max_length=100,null=True)
    wrongAnswer1=models.CharField(max_length=100,null=True)
    wrongAnswer2=models.CharField(max_length=100,null=True)
    wrongAnswer3=models.CharField(max_length=100,null=True)

class QuizDetail(models.Model):
    quizID = models.CharField(max_length=100,null=False,primary_key=False)
    date=models.DateTimeField(auto_now_add=True,null=True)
    question=models.ForeignKey(QuestionAnswer,null=True,on_delete=models.SET_NULL)
    givenAnswer=models.CharField(max_length=100,null=False)
    correct=models.BooleanField(default=False)
    quizDuration=models.CharField(max_length=100,null=False)
    userID=models.CharField(max_length=100,null=True)

    # def __str__(self) -> str:
    #     return str(self.id)+ " : "+self.question.question+ " : "+self.question.answer+  " : "+str(self.userID) + '\n'

    @staticmethod
    def genrateID(userInfo):
        return str(userInfo.id)+str(time.time())
    

class UserInfo(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,null=True)
    email=models.EmailField(null=True)
    password=models.CharField(max_length=15,null=True)
    quiz=models.ManyToManyField(QuizDetail)



