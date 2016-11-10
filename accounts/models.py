import os

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.template.defaultfilters import slugify
from django.conf import settings

from ShowCase.slugger import unique_slugify

from .usermanager import UserManager
from .picturehandler import bind_profile_picture_handler, WIDTH_PROFILE, resize_picture_path

from compositions.models import Composition
from streams.manager import follow_user
from .tasks import send_welcome_mail


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
    picture_major = models.CharField(max_length=7, default="#000000")

    login_type = models.CharField(default='NT', max_length=2, choices=LOGIN_CHOICES)

    follows = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='followers')

    nsfw = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args, **kwargs):
        new = False
        if self.pk is None:
            new = True

        unique_slugify(self, self.name)
        self.email = self.normalize_email(self.email)
        super(User, self).save(*args, **kwargs)

        if new and self.is_active:
            send_welcome_mail.delay(self.id)

    def get_absolute_url(self):
        return '/@' + self.slug

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
        return resize_picture_path(self.picture.url, suffix)

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

    def get_sitemap_url(self):
        return "http://thirddime.com/@{0}".format(self.slug)

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def followings_count(self):
        return self.follows.count()

    @property
    def paintings_count(self):
        return self.arts.count()

    @property
    def uploads_count(self):
        return self.compositions.count()

    @property
    def buckets_count(self):
        return self.buckets.filter(public=True).count()

    @property
    def drafts_count(self):
        return self.buckets.filter(public=False).count()

    @property
    def bookmarks_count(self):
        return self.bookmarks.count()

    @property
    def admirations_count(self):
        return self.admirations.count()

    def is_followed(self, user_id):
        return self.followers.filter(id=user_id).exists()

# Bind Signals
bind_profile_picture_handler(User)

def follow_staff_user(user):
    staff_user = User.objects.get(email='info@thirddime.com')
    user.follows.add(staff_user)
    follow_user(user.id, staff_user.id)

def user_created(sender, instance, created, raw, **kwargs):
    if created and not raw:
        follow_staff_user(instance)
        MailOptions.objects.create(user=instance)

post_save.connect(user_created, sender=User)


class MailOptions(models.Model):
    user = models.OneToOneField(User)
    admiration = models.BooleanField(default=True)
    to_bucket = models.BooleanField(default=True)
    follow = models.BooleanField(default=True)