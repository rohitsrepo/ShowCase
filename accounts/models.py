import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.template.defaultfilters import slugify
from django.conf import settings
from .usermanager import UserManager
from compositions.models import Composition
from .picturehandler import bind_profile_picture_handler, WIDTH_PROFILE
from ShowCase.slugger import unique_slugify


def get_upload_file_name_users(instance, filename):
    return 'Users/%s/Profile/%s' % (instance.name, instance.name + '.' + filename.split('.')[-1])


class User(AbstractBaseUser, PermissionsMixin):

    FACEBOOK = 'FB'
    TWITTER = 'TW'
    GOOGLE = 'GG'
    NATIVE = 'NT'
    LOGIN_CHOICES = (
        (FACEBOOK, 'facebook'),
        (TWITTER, 'twitter'),
        (GOOGLE, 'google'),
        (NATIVE, 'native'),
    )

    name = models.CharField(verbose_name='name', max_length=80)
    slug = models.SlugField(max_length=100, unique=True)
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

    bookmarks = models.ManyToManyField(Composition, related_name='bookers')

    follows = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='followers')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        self.email = self.normalize_email(self.email)
        super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()

    def has_default_picture(self):
        if settings.DEFAULT_USER_PICTURE not in self.picture.url:
            return False
        return True

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.name

    def _format_url(self, suffix):
        file_path, file_name = os.path.split(self.picture.url)
        name, extension = os.path.splitext(file_name)
        return os.path.join(file_path, '{0}_{1}{2}'.format(name, suffix, extension))

    def get_picture_url(self):
        return self._format_url(WIDTH_PROFILE)

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

    def get_sitemap_url(self):
        return "http://thirddime.com/@{0}".format(self.slug)

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def followings_count(self):
        return self.follows.all().count()

    @property
    def paintings_count(self):
        return self.arts.all().count()

    @property
    def uploads_count(self):
        return self.compositions.all().count()

    def is_followed(self, user_id):
        return self.followers.filter(id=user_id).exists()

# Bind Signals
bind_profile_picture_handler(User)