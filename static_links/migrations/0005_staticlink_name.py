# Generated by Django 3.2.2 on 2021-05-21 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_links', '0004_remove_staticlink_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticlink',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]