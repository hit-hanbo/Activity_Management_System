from django.db import models

# Create your models here.


class Volunteer(models.Model):
    name_zh = models.CharField(max_length=20)
    stu_id = models.CharField(max_length=20, unique=True)
    phone_num = models.CharField(max_length=20)
    time_volunteer = models.IntegerField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.stu_id)


class Activity(models.Model):
    title = models.CharField(max_length=20, unique=True)
    group = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class MyActivity(models.Model):
    mytime = models.IntegerField()
    person = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
