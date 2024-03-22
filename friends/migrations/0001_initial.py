# Generated by Django 3.2.23 on 2024-03-22 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('requested', 'Following Requested'), ('accepted', 'Follower')], max_length=50, verbose_name='Following status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='profiles.userprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to='profiles.userprofile')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('user', 'follower')},
            },
        ),
    ]
