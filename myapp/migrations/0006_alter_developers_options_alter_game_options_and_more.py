# Generated by Django 5.1.3 on 2024-12-06 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_developers_options_alter_game_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='developers',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='gamegenres',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='gameplayers',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='genres',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='platforms',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='publishers',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='userfollowers',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='userfollowing',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'managed': False},
        ),
    ]