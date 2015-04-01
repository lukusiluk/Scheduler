from django.db import models

class Activity(models.Model):
    code = models.IntegerField(max_length=10)
    Hour = models.CharField(max_length=200)
    Day = models.CharField(max_length=200)
    Subject = models.CharField(max_length=200)
    Teachers = models.CharField(max_length=200)
    Students = models.CharField(max_length=200)
    Tag = models.CharField(max_length=200)
    Room = models.CharField(max_length=200)
    Comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '%s %s %s %s' % (self.Subject, self.Tag, self.Teachers, self.Room,)

class Groups(models.Model):
    wyklad = models.CharField(max_length=10)
    cwiczenia = models.CharField(max_length=10)
    laboratoryjna = models.CharField(max_length=10)

    def __str__(self):
        return '%s %s %s' % (self.wyklad, self.cwiczenia, self.laboratoryjna)
