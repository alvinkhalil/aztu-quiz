from django.contrib.auth.models import User
from django.db import models
from django.db.models import deletion
from django.db.models.deletion import CASCADE

# Create your models here.

class QuestionModel(models.Model):

    user = models.ForeignKey(User, on_delete=CASCADE)

    name = models.CharField(max_length=200, verbose_name="Sual",null=True)
    a = models.CharField(max_length=200, verbose_name="A)",null=True)
    b = models.CharField(max_length=200, verbose_name="B)",null=True)
    c = models.CharField(max_length=200, verbose_name="C)",null=True)
    d = models.CharField(max_length=200, verbose_name="D)",null=True)
    
    answer = models.CharField(max_length=200,verbose_name="Cavab:")


    def __str__(self):
        return self.name


class ResultsModel(models.Model):

    user = models.ForeignKey(User, on_delete=CASCADE)
    score = models.CharField(max_length=1)
    correct = models.IntegerField()
    wrong = models.IntegerField()

    def __str__(self):

        return self.user.username
