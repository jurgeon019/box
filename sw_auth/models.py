import unicodedata

from django.utils.translation import gettext_lazy as _
from django.db import models 
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.contrib.auth.models import (
  Group,
  Permission,
  UserManager,
  UnicodeUsernameValidator, 
  _user_has_module_perms,
)
from django.utils import timezone 
from django.utils.crypto import get_random_string, salted_hmac
from django.core.mail import send_mail


class AbstractUser(models.Model):
    gender_choices = [
      ["u",_("Невідомо")],
      ["m",_("Чоловік")],
      ["f",_("Жінка")],
    ]
    username_validator = UnicodeUsernameValidator()
    password     = models.CharField(
        _('password'), max_length=128,
    )
    phone_number = models.CharField(
        _("Номер телефону"), max_length=255, 
        blank=True, null=True,
    )
    address      = models.TextField(
        _("Адреса"), blank=True, null=True,
    )
    birth_date   = models.DateTimeField(
        _("Дата народження"), blank=True, null=True,
    )
    gender       = models.CharField(
        _("Стать"), choices=gender_choices, 
        max_length=20, default="m",
    )
    first_name   = models.CharField(
        _('first name'), 
        max_length=30, blank=True, null=True,
    )
    last_name    = models.CharField(
        _('last name'), 
        max_length=150, blank=True, null=True,
    )
    email        = models.EmailField(
        _('email address'), blank=True)
    group        = models.ForeignKey(
        to="customer.CustomerGroup", 
        verbose_name=_("Група"), 
        blank=True, null=True, 
        on_delete=models.SET_NULL, 
        help_text=("Група з купонами на скидку"),
    )
    username     = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_staff     = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active    = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups       = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login  = models.DateTimeField(_('last login'), blank=True, null=True)
    objects     = UserManager()
    _password   = None
    EMAIL_FIELD     = 'email'
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def __str__(self):
      return f"{self.username}, {self.get_full_name()}"
      return f"{self.first_name} {self.last_name} ({self.username}, {self.phone_number}, {self.email})"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'user')

    def get_group_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'group')

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'all')

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True



