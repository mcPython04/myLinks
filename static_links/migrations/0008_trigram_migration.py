from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('static_links', '0007_alter_staticlink_file'),
    ]

    operations = [
        TrigramExtension(),
    ]