from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, nickname, firstname, lastname, email, password=None):
        if nickname is None:
            raise TypeError("The user must have a nickname")

        if email is None:
            raise TypeError("The user must have a email")

        if firstname is None:
            raise TypeError("The user must have a firstname")

        if lastname is None:
            raise TypeError("The user must have a lastname")

        user = self.model(nickname=nickname, email=self.normalize_email(email), firstname=firstname, lastname=lastname)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, nickname, firstname, lastname, email, password=None):
        if password is None:
            raise TypeError("Administrator must have a password")

        user = self.create_user(nickname, firstname, lastname, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    nickname = models.CharField(db_index=True, unique=True, max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "firstname", "lastname"]

    objects = UserManager()

    @property
    def refresh_token(self):
        return str(RefreshToken.for_user(self))

    @property
    def access_token(self):
        return str(RefreshToken.for_user(self).access_token)

    def __str__(self):
        return self.email
