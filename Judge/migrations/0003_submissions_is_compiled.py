# Generated by Django 5.2 on 2025-05-05 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Judge', '0002_alter_submissions_solution_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissions',
            name='is_compiled',
            field=models.BooleanField(default=False),
        ),
    ]
