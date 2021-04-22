from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    is_manager = models.BooleanField(
        default=False,
        help_text="Designates that this user has permissions to make transactions."
    )

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username


class StudentUser(CustomUser):
    class Meta:
        verbose_name = "Student"
        proxy = True

    def __str__(self):
        return self.student.enrollment_no


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student', primary_key=True)
    enrollment_no = models.CharField(max_length=20, unique=True)
    std = models.CharField(max_length=5)
    tokens = models.DecimalField(max_digits=10, decimal_places=2)

    def get_balance(self):
        return f"₹ {self.tokens}"

    def __str__(self):
        return self.enrollment_no
