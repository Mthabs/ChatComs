# Generated by Django 3.2.23 on 2024-03-24 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollowing',
            name='status',
            field=models.CharField(choices=[('requested', 'Following Requested'), ('accepted', 'Follower')], default='requested', max_length=50, verbose_name='Following status'),
        ),
    ]
