from lib2to3.pytree import Base
from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager, AbstractBaseUser)
# Create your models here.

# 표준 User model
class User(AbstractUser):
    pass
