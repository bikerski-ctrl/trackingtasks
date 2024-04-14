from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done")
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ]

    URGENCY_CHOICES = [
        ("very", "Very Urgent"),
        ("urgent", "Urgent"),
        ("not_very", "Not Very Urgent"),
        ("not", "Not Urgent"),
    ]

    title = models.CharField(max_length=63)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    urgency = models.CharField(max_length=32, choices=URGENCY_CHOICES, blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")


    def __str__(self):
        return str(self.title)