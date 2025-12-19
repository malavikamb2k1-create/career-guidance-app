from django.db import models
from django.contrib.auth.models import User

class College(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    housing_fee = models.DecimalField(max_digits=10, decimal_places=2)
    eligibility = models.CharField(max_length=300)
    ranking = models.IntegerField()
    scholarships = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AptitudeQuestion(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class TestResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)
