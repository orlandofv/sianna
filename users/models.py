from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext as _
from django.core import exceptions
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


SEX_CHOICES = (
    (1, _("Masculino")),
    (2, _("Femenino"))
)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('User must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """We change the default user auth by email auth"""

    username = None
    email = models.EmailField(_('Email'), unique=True, help_text=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.email) or ''


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(null=False, blank=False, help_text=False, verbose_name=_("Nome do Usuário"),
                                 max_length=20, unique=True)
    contacto = PhoneNumberField(verbose_name=_('Telefone'), null=True, help_text=False, blank=True)
    data_nascimento = models.DateField(_('Data de Nascimento'), help_text=False, null=True, blank=True)
    sexo = models.IntegerField(verbose_name=_('Sexo'), choices=SEX_CHOICES, default=1, help_text=False)
    terms = models.BooleanField(verbose_name=_("Termos"), help_text=False)

    def save(self, *args, **kwargs):
        if self.terms is False:
            self.save(commit=False)
            raise exceptions.ValidationError(_("Please accept our terms and conditions to create Account!'"))

        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.email) or ''




