# Generated by Django 3.2.2 on 2021-05-21 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('static_links', '0003_alter_staticlink_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staticlink',
            name='name',
        ),
    ]