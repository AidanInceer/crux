from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Plan(models.Model):
    name = models.CharField(max_length=100, default="Training Plan")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1


class ActivityType(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(
        max_length=20, default="#0d6efd", help_text="Hex color code"
    )
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ["name"]  # Just name unique now

    def __str__(self):
        return self.name


class TrainingSession(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="sessions")
    activity_type = models.ForeignKey(
        ActivityType, on_delete=models.CASCADE, related_name="sessions"
    )
    date = models.DateField()
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["date"]
        unique_together = ["plan", "date", "activity_type"]

    def __str__(self):
        return f"{self.activity_type.name} on {self.date}"

    @property
    def is_past_due(self):
        return self.date < date.today() and not self.completed
