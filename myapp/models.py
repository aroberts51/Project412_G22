# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Developers(models.Model):
    developerid = models.IntegerField(primary_key=True)
    developername = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'developers'


class Game(models.Model):
    gameid = models.IntegerField(primary_key=True)
    gamename = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    coverurl = models.CharField(max_length=512, blank=True, null=True)
    publisherid = models.ForeignKey(
        'Publishers', models.SET_NULL, db_column='publisherid', blank=True, null=True
    )
    releasedate = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game'


class Gamegenres(models.Model):
    gameid = models.ForeignKey(
        Game, models.CASCADE, db_column='gameid'
    )  # The composite primary key (gameid, genreid) found, that is not supported. The first column is selected.
    genreid = models.ForeignKey('Genres', models.CASCADE, db_column='genreid')

    class Meta:
        managed = False
        db_table = 'gamegenres'
        unique_together = (('gameid', 'genreid'),)


class Gameplayers(models.Model):
    username = models.ForeignKey(
        'Users', models.CASCADE, db_column='username'
    )
    gameid = models.ForeignKey(
        'Game', models.CASCADE, db_column='gameid'
    )

    class Meta:
        managed = False
        db_table = 'gameplayers'
        unique_together = (('username', 'gameid'),)


class Genres(models.Model):
    genreid = models.IntegerField(primary_key=True)
    genrename = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'genres'


class Platforms(models.Model):
    platformid = models.IntegerField(primary_key=True)
    platformname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'platforms'


class Publishers(models.Model):
    publisherid = models.IntegerField(primary_key=True)
    publishername = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'publishers'


class Userfollowers(models.Model):
    username = models.ForeignKey(
        'Users', models.CASCADE, db_column='username'
    )  # The composite primary key (username, followerusername) found, that is not supported. The first column is selected.
    followerusername = models.ForeignKey(
        'Users', models.CASCADE, db_column='followerusername', related_name='userfollowers_followerusername_set'
    )

    class Meta:
        managed = False
        db_table = 'userfollowers'
        unique_together = (('username', 'followerusername'),)


class Userfollowing(models.Model):
    username = models.ForeignKey(
        'Users', models.CASCADE, db_column='username'
    )  # The composite primary key (username, followingusername) found, that is not supported. The first column is selected.
    followingusername = models.ForeignKey(
        'Users', models.CASCADE, db_column='followingusername', related_name='userfollowing_followingusername_set'
    )

    class Meta:
        managed = False
        db_table = 'userfollowing'
        unique_together = (('username', 'followingusername'),)


class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    useremail = models.CharField(unique=True, max_length=50)
    userpassword = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'
