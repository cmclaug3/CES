from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager




class UserManager(BaseUserManager):
    def create_user(self, email, first_name='', last_name='', password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("users must have an email address")
        # if not password:
        #     raise ValueError("users must set a password")

        user_obj = self.model(
            email=self.normalize_email(email)
        )

        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.first_name = first_name
        user_obj.last_name = last_name

        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, first_name='', last_name='', password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        return user

    def create_superuser(self, email, first_name='', last_name='', password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    time_stamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email and password are included by default

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_active(self):
    #     return self.active
    #
    # @property
    # def is_staff(self):
    #     return self.staff
    #
    # @property
    # def is_admin(self):
    #     return self.admin





class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6, default=0000, blank=True, null=True)

    def get_full_name(self):
        return self.user.get_full_name()

    def get_short_name(self):
        return self.user.get_short_name()

    def __str__(self):
        return self.get_full_name()





USER_TYPES = (
    ('employee', 'Employee'),
    ('admin', 'Admin'),
    ('superuser', 'Superuser'),
)

class PreSetAuthorizedUser(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=255)
    code = models.CharField(max_length=15)
    type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
