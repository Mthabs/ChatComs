# Generated by Django 3.2.23 on 2024-03-23 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_commentlikes_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='likes',
            options={'ordering': ['-created_at']},
        ),
    ]