from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True) #make email unique


class Profile(models.Model):
    # OneToOne = one user has exactly one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= "profile")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)


    def __str__(self):
        return self.user.username
