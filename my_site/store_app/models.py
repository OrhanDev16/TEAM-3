from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

USER_STATUS = (
    ('beginner', 'beginner'),
    ('active', 'active'),
    ('pro', 'pro')
)

Priority = (('low', 'low'),
            ('medium', 'medium'),
            ('high','high'),
            )

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(14),
                                                       MaxValueValidator(70)])
    phone_number = PhoneNumberField(default='+996', )
    avatar = models.ImageField(upload_to='profiles_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=USER_STATUS, default='beginner')
    date_registered = models.DateField(auto_now_add=True)

class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)

class Task(models.Model):
    title = models.CharField(max_length=100)
    decription = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=Priority, default='medium')
    deadline = models.DateField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    assignee = models.ForeignKey(UserProfile,null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)