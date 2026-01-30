from django.contrib import admin

from .models import ActivityType, Plan, TrainingSession


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "duration_days")


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "color")


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ("plan", "date", "activity_type", "completed", "is_past_due")
    list_filter = ("plan", "completed", "activity_type")
    ordering = ("date",)
