from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):    
   
   use_in_migrations = True    
   
   def create_user(self, name, generation, management_team_status, email, department, access_token, refresh_token, password):        
       
       if not email:            
           raise ValueError('must have user email')
       if not password:            
           raise ValueError('must have user password')

       user = self.model(  
           name = name,          
           generation = generation,     
           management_team_status = management_team_status,
           email = email,    
           department = department, 
           access_token = access_token,
           refresh_token = refresh_token, 
       )        
       user.set_password(password)   
       user.is_admin = True
       user.is_active = True  
       user.save(using=self._db)        
       return user

   def create_superuser(self, name, generation, management_team_status, email, department, access_token, refresh_token, password):        
   
       user = self.create_user( 
           name = name,  
           generation = generation,     
           management_team_status = management_team_status,
           email = email,    
           department = department, 
           access_token = access_token,
           refresh_token = refresh_token,                  
           password=password        
       )
       user.is_admin = True
       user.is_superuser = True
       user.is_active = True
       user.save(using=self._db)
       return user 


class User(AbstractBaseUser, PermissionsMixin):    
   
   objects = UserManager()
   
   name = models.CharField(max_length=10, blank=True, null=True)
   generation = models.IntegerField(blank=True, null=True)
   email = models.CharField(max_length=254, unique=True, blank=True, null=True)
   department = models.IntegerField(blank=True, null=True)
   access_token = models.CharField(max_length=300)
   refresh_token = models.CharField(max_length=300)
   authentication_number = models.CharField(max_length=6, blank=True, null=True)

   is_active = models.BooleanField(default=False)
   is_admin = models.BooleanField(default=False)

   USERNAME_FIELD = 'email'    
   REQUIRED_FIELDS = [
       'name',
       'generation',
       'department',
       'access_token',
       'refresh_token'
   ]

   def __str__(self):
       return self.email

   @property
   def is_staff(self):
       return self.is_admin
    
    