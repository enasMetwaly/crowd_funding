from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
PHONE_REGEX = RegexValidator(
    r'^01[0-2][0-9]{8}$', 'Egyptian phone number is required')


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name='', password=None, is_active=True, is_staff=False, is_admin=False):

        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not first_name:
            raise ValueError("Users must have a first name")

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, first_name, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, first_name, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, verbose_name='email', unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField( blank=True, null=True, verbose_name='last login')
    date_joined = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=20, verbose_name='first name')
    last_name = models.CharField(
        max_length=20, default='', verbose_name='last name')

    phone = models.CharField(max_length=15, validators=[
        PHONE_REGEX], verbose_name='phone')
    avatar = models.ImageField(
        upload_to="profile_images", verbose_name='profile picture')
    country = models.CharField(
        max_length=20, blank=True, default='', verbose_name='country')
    birthdate = models.DateField(
        blank=True, null=True, verbose_name='birthdate')
    fb_account = models.URLField(blank=True)

    groups = models.ManyToManyField(
        Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_user_permissions', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    EMAIL_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)

    def get_full_name(self):
        if self.__str__:
            return self.__str__
        return self.email

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        try:
            existing_user = User.objects.get(pk=self.pk)
            if existing_user.avatar != self.avatar:
                user_profile, created = UserProfile.objects.get_or_create(user=self)
                user_profile.avatar = self.avatar
                user_profile.save()
        except User.DoesNotExist:
            pass

        super(User, self).save(*args, **kwargs)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    avatar = models.ImageField(upload_to="profile_images", verbose_name='profile picture'                       )

    def get_absolute_url(self):
        return reverse('user_profile')
