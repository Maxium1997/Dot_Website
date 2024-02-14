from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class Song(models.Model):
    serial_number = models.CharField(max_length=8, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    source_url = models.URLField()

    def __str__(self):
        return self.title


class Booth(models.Model):
    number = models.CharField(max_length=6, null=False, blank=False)
    maximum_participant_number = models.PositiveSmallIntegerField()
    starting_time = models.DateTimeField()
    duration = models.PositiveSmallIntegerField()
    creator = models.CharField(max_length=255, null=False, blank=False)

    play_list = GenericRelation(Song)

    def __str__(self):
        return self.number
