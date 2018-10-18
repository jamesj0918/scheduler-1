from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    grade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)], default=1
    )
