# Generated by Django 3.2.20 on 2023-08-14 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0004_alter_userprofile_friends'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='username',
            new_name='email',
        ),
    ]
