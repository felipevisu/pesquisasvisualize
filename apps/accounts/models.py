import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

from apps.clients.models import Client


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    ADMINISTRATOR = 'administrator'
    CLIENT = 'client'
    INTERVIEWER = 'interviewer'

    TYPES = (
        (ADMINISTRATOR, 'Administrador'),
        (CLIENT, 'Cliente'),
        (INTERVIEWER, 'Entrevistador')
    )

    username = models.CharField(
        'nome de usuário', max_length=50, unique=True,
        validators=[
            validators.RegexValidator(re.compile("^[\w.@+-]+$"),
                'Informe um nome de usuário válido.'
                'Este valor deve conter apenas letras, números e os caracteres: @/./+/-/_ .',
                'invalid'
            )
        ],
        help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
    )
    
    first_name = models.CharField('primeiro nome', max_length=100, blank=True, null=True)
    last_name = models.CharField('sobrenome', max_length=100, blank=True, null=True)
    email = models.EmailField('e-mail', unique=True) 
    is_staff = models.BooleanField('equipe', default=False)
    is_active = models.BooleanField('ativo', default=True)
    date_joined = models.DateTimeField('data de entrada', auto_now_add=True)
    # Seleciona uma opção somente se o usuário for do tipo Cliente
    user_type = models.CharField('tipo de usuário', max_length=100, choices=TYPES, default=ADMINISTRATOR)
    client = models.ForeignKey(Client, verbose_name='cliente', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        return self.get_short_name()

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.username