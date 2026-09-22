from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class UserProfile(AbstractUser):
    STATUS_BEGINNER = "beginner"
    STATUS_ACTIVE = "active"
    STATUS_PRO = "pro"
    STATUS_CHOICES = [
        (STATUS_BEGINNER, "Beginner"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_PRO, "Pro"),
    ]

    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(14), MaxValueValidator(70)],
    )
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_BEGINNER
    )
    date_register = models.DateField(auto_now_add=True)

    def str(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_img = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["category_name"]

    def str(self):
        return self.category_name


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, related_name="projects", on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        UserProfile, related_name="projects", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]

    def str(self):
        return self.project_name

    def get_tasks_count(self):
        return self.tasks.count()

    def get_completed_percent(self):
        total = self.get_tasks_count()
        if total == 0:
            return 0
        completed = self.tasks.filter(completed=True).count()
        return round(completed / total * 100)


