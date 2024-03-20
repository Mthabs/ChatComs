# Generated by Django 3.2.23 on 2024-03-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20240315_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image_filter',
            field=models.CharField(blank=True, choices=[('normal', 'Normal'), ('black_and_white', 'Black and White'), ('sepia', 'Sepia'), ('vintage', 'Vintage'), ('grayscale', 'Grayscale'), ('warm', 'Warm Tone'), ('cool', 'Cool Tone'), ('invert', 'Invert Colors'), ('blur', 'Blur'), ('sharpen', 'Sharpen')], default='normal', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]