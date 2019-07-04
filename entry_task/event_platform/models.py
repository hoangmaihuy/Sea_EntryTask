from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=256)
    salt = models.CharField(max_length=20)
    role = models.IntegerField()

    class Meta:
        db_table = 'user_tab'
        indexes = [models.Index(fields=['username'])]


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'category_tab'
        indexes = [models.Index(fields=['category_name'])]


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.IntegerField()
    by_user = models.IntegerField()
    content = models.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_tab'
        indexes = [models.Index(fields=['event_id'])]


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()
    photo_url = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'event_tab'
        ordering = ['-date']
        indexes = [models.Index(fields=['-date'])]


class EventCategoryMap(models.Model):
    event_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        db_table = 'event_category_tab'
        indexes = [models.Index(fields=['category_id', 'event_id'])]


class EventParticipantMap(models.Model):
    event_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        db_table = 'event_participant_tab'
        indexes = [models.Index(fields=['event_id'])]


class EventLikeMap(models.Model):
    event_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        db_table = 'event_like_tab'
        indexes = [models.Index(fields=['event_id'])]

