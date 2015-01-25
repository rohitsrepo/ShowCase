# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import accounts.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('compositions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=40, verbose_name=b'first name')),
                ('last_name', models.CharField(max_length=40, verbose_name=b'last name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address')),
                ('about', models.TextField(verbose_name=b'descriotion', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designate whether user can login into admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Desgnates whether a registered user can login.', verbose_name=b'active status')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name=b'date user joined with us')),
                ('picture', models.ImageField(default=b'/media/root/user_default.jpg', upload_to=accounts.models.get_upload_file_name_users)),
                ('bookmarks', models.ManyToManyField(related_name=b'collectors', to='compositions.Composition')),
                ('follows', models.ManyToManyField(related_name=b'followers', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
    ]
