from django.db import models
from web_app.models import Post
from django.utils import timezone
from PIL import Image

# ------ 1 login veikia -------
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth import get_user_model

# ------ 2 ir 3 login veikia (užkomentuoti naudojant 1 login variantą) -------
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError


# Create your models here.
# ------ 2 ir 3 login variantams ------
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        # model = User.objects.get()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            raise ValidationError("Įvesti neteisingi duomenys.")
            # return None
            # ------- 3 --------
            # error_message = "Įvesti neteisingi duomenys."
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None


# ---------- 1 login veikia (šitam nereikia EmailBackend) ------------
# ----------- reikia keist pati User modeli ir UserManager ------------
# class UserManager(BaseUserManager):
#     def create_user(
#         self,
#         email,
#         username,
#         password=None,
#         is_active=True,
#         is_staff=False,
#         is_admin=False,
#     ):  # put here all REQUIRED FIELDS
#         if not email:
#             raise ValueError("Users must have an email address")
#         if not password:
#             raise ValueError("Users must have a password")

#         user_obj = self.model(
#             email=self.normalize_email(email)
#         )  # Normalizes email addresses by lowercasing the domain portion of the email address.
#         user_obj.set_password(password)  # set password or change user password
#         user_obj.username = username
#         user_obj.staff = is_staff
#         user_obj.admin = is_admin
#         user_obj.active = is_active
#         user_obj.save(using=self._db)
#         return user_obj

#     def create_staffuser(self, email, password=None):
#         user = self.create_user(email, username, password=password, is_staff=True)
#         return user

#     def create_superuser(self, email, username=None, password=None):
#         user = self.create_user(
#             email, username, password=password, is_staff=True, is_admin=True
#         )
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(verbose_name="El. paštas", max_length=255, unique=True)
#     username = models.CharField(max_length=100, unique=True, null=True)
#     # fullname = models.CharField(max_length=255, blank=True, null=True)
#     active = models.BooleanField(default=True)  # can login
#     staff = models.BooleanField(default=False)  # staff user non superuser
#     admin = models.BooleanField(default=False)  # superuser
#     timestamp = models.DateTimeField(default=timezone.now)
#     # confirm     = models.BooleanField(default=False)
#     # confirmed_date     = models.DateTimeField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = [
#         "username"
#     ]  # Email & Password are required by default, we add username.

#     def __str__(self):
#         return self.email

#     def get_full_name(self):
#         return self.email

#     def get_short_name(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     @property
#     def is_staff(self):
#         return self.staff

#     @property
#     def is_admin(self):
#         return self.admin

#     @property
#     def is_active(self):
#         return self.active


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, verbose_name="About Me")
    image = models.ImageField(default="default_pic.jpg", upload_to="profile_pics/")
    # video = models.ForeignKey(
    #    Post, on_delete=models.CASCADE, null=True, blank=True
    # )

    def __str__(self):
        return f"{self.user.username} Profile"

    # automatically resize the uploaded image:
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        # if we get "cannot write mode P as JPEG" error, convert to RGB:
        if img.mode != "RGB":
            img = img.convert("RGB")
        if img.height > 96 and img.width > 96:
            output_size = (96, 96)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.TextField(max_length=400, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f'Comment: "{self.comment}" by {self.posted_by}'


class Like(models.Model):

    LIKE = "Patinka"
    UNLIKE = "Daugiau nepatinka"

    LIKE_CHOICES = [
        (LIKE, "Patinka"),
        (UNLIKE, "Daugiau nepatinka"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default="Patinka", max_length=25)

    def __str__(self):
        return str(self.post)
