from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings
from compositions.models import Composition
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

    def create_artist(self, name):
        holder = str(uuid.uuid1())
        return self.create_user(
            holder+'@user.com',
            name,
            holder,
            is_active = False,
            is_artist = True
        )


def get_upload_file_name_users(instance, filename):
    return 'Users/%s/Profile/%s' % (instance.id, instances.name + filename.split('.')[-1])


class User(AbstractBaseUser, PermissionsMixin):

    FACEBOOK = 'FB'
    TWITTER = 'TW'
    NATIVE = 'NT'
    LOGIN_CHOICES = (
        (FACEBOOK, 'facebook'),
        (TWITTER, 'twitter'),
        (NATIVE, 'native'),
    )

    name = models.CharField(verbose_name='name', max_length=80)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    about = models.TextField(verbose_name='descriotion', blank=True,)
    is_staff = models.BooleanField(verbose_name='staff status',
                                   default=False, help_text='Designate whether user can login into admin site.',)
    is_artist = models.BooleanField(verbose_name='artist status',
                                   default=False, help_text='Designate whether user is an artist.',)
    is_active = models.BooleanField(verbose_name='active status',
                                    default=True, help_text='Desgnates whether a registered user can login.',)
    date_joined = models.DateTimeField(verbose_name='date user joined with us',
                                       auto_now_add=True,)

    picture = models.ImageField(
        upload_to=get_upload_file_name_users, default=settings.DEFAULT_USER_PICTURE)

    login_type = models.CharField(default='NT', max_length=2, choices=LOGIN_CHOICES)

    bookmarks = models.ManyToManyField(Composition, related_name='collectors')

    follows = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='followers')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args, **kwargs):
        self.email = self.normalize_email(self.email)
        super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        # send_mail(subject, message, from_email, [self.email])

    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """

        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            raise Exception(
                "Invalid email id recieved during mormalization %s" % (ValueError))
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def get_absolute_url(self):
        """
        Return link to user profile(Showcase)
        """

        return "#/{0}".format(self.id)
