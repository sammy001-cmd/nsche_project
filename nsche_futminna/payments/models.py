# payments/models.py
from django.db import models
from accounts.models import StudentProfile

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # store in kobo (1000 NGN = 100000)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    description = models.CharField(max_length=255, blank=True, null=True)  # optional
    payment_method = models.CharField(max_length=50, default="paystack")  # future-proof
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # track status updates

    def __str__(self):
        # Correct: no parentheses for property
        return f"{self.student.user.username} - {self.status} - {self.amount_naira:.2f} NGN"

    @property
    def amount_naira(self):
        return self.amount / 100  # keep decimals, e.g. 1500.00



