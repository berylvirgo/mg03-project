from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_superuser(self,email,password,name,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_author',True)


        if other_fields.get('is_staff') is not True:
            return ValueError('Superuser must be assign is_staff=True')

        if other_fields.get('is_superuser') is not True:
            return ValueError('Superuser must be assign is_superuser=True')

        if other_fields.get('is_author') is not True:
            return ValueError('Superuser must be assign is_author=True')

        return self.create_user(email,password,name,**other_fields)


    def create_author(self,email,password,name,**other_fields):
        other_fields.setdefault('is_staff',False)
        other_fields.setdefault('is_superuser',False)
        other_fields.setdefault('is_author',True)

        if other_fields.get('is_author') is not True:
            return ValueError('Author must be assign is_author=True')

        return self.create_user(email,password,name,**other_fields)


    def create_user(self,email,password,name,**other_fields):

        if not email:
            raise ValueError('You must provide a valid email')

        email = self.normalize_email(email)

        user = self.model(email=email,name=name,**other_fields)

        user.set_password(password)

        user.save()

        return user
        

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=225,null=True,blank=True)
    username = models.CharField(max_length=225,null=True,blank=True)
    email = models.EmailField(max_length=225,unique=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='users/', default="default.png")
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    # is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name



