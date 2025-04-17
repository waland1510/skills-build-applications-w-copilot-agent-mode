from djongo import models
from bson import ObjectId

class User(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    class Meta:
        db_table = 'users'

class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=255)
    members = models.JSONField()
    class Meta:
        db_table = 'teams'

class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user_id = models.CharField(max_length=24)  # Store ObjectId as string
    type = models.CharField(max_length=50)
    duration = models.IntegerField()
    date = models.DateField()
    class Meta:
        db_table = 'activity'

class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    team_id = models.CharField(max_length=24)  # Store ObjectId as string
    points = models.IntegerField()
    class Meta:
        db_table = 'leaderboard'

class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        db_table = 'workouts'