from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):

    def create_user_base(self, email, name, password, is_staff, is_superuser, **extra_fields):
        '''
        Creates user with give email, name, password and staffing status.
        '''

        now = timezone.now()

        if not email:
            raise ValueError('User must have an email address')
        else:
            email = self.normalize_email(email)

        if not name:
            raise ValueError('User must have name.')

        user = self.model(email=email, name=name, last_login=now,
                          is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password=None, **extra_fields):
        '''
        Creates and save non-staff-normal user with given email, name and password.
        '''

        return self.create_user_base(email, name, password, False, False, **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        '''
         Creates and saves super user with given email, name and password.
        '''
        return self.create_user_base(email, name, password, True, True, **extra_fields)

    def create_artist(self, name, **extra_fields):
        holder = str(uuid.uuid1())
        return self.create_user(
            holder+'@user.com',
            name,
            holder,
            is_active = False,
            is_artist = True,
            **extra_fields
        )
