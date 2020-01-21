from django.db import models
from django.shortcuts import reverse 
from django.contrib.auth import get_user_model 


User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=255)


class Priority(models.Model):
    title = models.CharField(max_length=255)


class Schedule(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField()


class Event(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField()


class Goal(models.Model):
    actions     = models.ManyToManyField(to='helper.Action', related_name='goals')
    title       = models.CharField(max_length=255)
    description = models.TextField()
    priority    = models.ForeignKey(to=Priority, blank=True, null=True, on_delete=models.SET_NULL, related_name='goals')
    parent      = models.ForeignKey(to='self', blank=True, null=True, on_delete=models.SET_NULL, related_name='subgoals')


class Task(models.Model):
    user        = models.ForeignKey(to=User, related_name='tasks', on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    description = models.TextField()
    done        = models.BooleanField(default=False)
    priority    = models.ForeignKey(to=Priority, blank=True, null=True, on_delete=models.SET_NULL, related_name='tasks')


class Action(models.Model):
    title      = models.CharField(max_length=255)
    user       = models.ForeignKey(to=User, related_name='actions', on_delete=models.CASCADE)
    last_start = models.DateTimeField()
    last_end   = models.DateTimeField()
    total      = models.TimeField()
    done       = models.BooleanField(default=False)


class Habbit(models.Model):
    user  = models.ForeignKey(to=User, related_name='habbits', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class Finance(models.Model):
    user  = models.ForeignKey(to=User, related_name='finances', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class Reminder(models.Model):
    user  = models.ForeignKey(to=User, related_name='reminders', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class Note(models.Model):
    user    = models.ForeignKey(to=User, related_name='notes', on_delete=models.CASCADE)
    title   = models.CharField(max_length=255)
    content = models.TextField()


class Skill(models.Model):
    user  = models.ForeignKey(to=User, related_name='skills', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)







