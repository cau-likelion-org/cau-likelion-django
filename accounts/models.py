from lib2to3.pytree import Base
from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager, AbstractBaseUser)
# Create your models here.

# 표준 User model
class User(AbstractUser):
    pass

# custom user
class UserManager(BaseUserManager):
    def create_user(self, name, generation, accessToken, refreshToken):
        if not name:
            raise ValueError('Users mush have name')
        if not generation:
            raise ValueError('Users must have generation')
        
        user = self.model(
            name = name,
            generation = generation,
            accessToken = accessToken,
            refreshToken = refreshToken,
        )

        user.save(using=self._db)
        return user