from django.db import models

# Create your models here.


class Volunteer(models.Model):
    name_zh = models.CharField(max_length=20)
    stu_id = models.CharField(max_length=20, unique=True)
    phone_num = models.CharField(max_length=20)
    time_volunteer = models.IntegerField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.stu_id

