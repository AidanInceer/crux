from datetime import date, timedelta

# from django.contrib.auth.decorators import login_required # Removed
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActivityTypeForm, PlanForm
from .models import ActivityType, Plan, TrainingSession


def index(request):
    plans = Plan.objects.all()
    return render(request, "planner/index.html", {"plans": plans})


def plan_create(request):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            # plan.user = request.user # Removed
            plan.save()
            messages.success(request, "Plan created successfully!")
            return redirect("plan_detail", plan_id=plan.id)
    else:
        form = PlanForm()
    return render(
        request, "planner/plan_form.html", {"form": form, "title": "Create Plan"}
    )


def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)  # Removed user=request.user

    # Generate dates
    total_days = (plan.end_date - plan.start_date).days + 1
    dates = [plan.start_date + timedelta(days=i) for i in range(total_days)]

    # Fetch activity types
    activity_types = ActivityType.objects.all()  # Removed filtering by user

    # Fetch sessions efficiently
    sessions = TrainingSession.objects.filter(plan=plan)
    # Organize sessions by date and activity_type_id for easy lookup in template
    session_map = {}
    for s in sessions:
        if s.date not in session_map:
            session_map[s.date] = {}
        session_map[s.date][s.activity_type.id] = s

    # Calculate Progress
    today = date.today()
    completed_count = sessions.filter(completed=True).count()
    total_sessions_count = sessions.count()

    if plan.start_date <= today <= plan.end_date:
        expected_so_far = sessions.filter(date__lte=today).count()
        diff = completed_count - expected_so_far
        if diff > 0:
            status = "Ahead"
            status_color = "success"
        elif diff < 0:
            status = "Behind"
            status_color = "danger"
        else:
            status = "On Track"
            status_color = "success"
    else:
        diff = 0
        status = "Not Active"
        status_color = "secondary"

    context = {
        "plan": plan,
        "dates": dates,
        "activity_types": activity_types,
        "session_map": session_map,
        "today": today,
        "completed_count": completed_count,
        "total_sessions_count": total_sessions_count,
        "status": status,
        "diff": abs(diff),
        "status_color": status_color,
    }
    return render(request, "planner/plan_detail.html", context)


def activity_list(request):
    activities = ActivityType.objects.all()  # Removed user filtering
    return render(request, "planner/activity_list.html", {"activities": activities})


def activity_create(request):
    if request.method == "POST":
        form = ActivityTypeForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            # activity.user = request.user # Removed
            activity.save()
            messages.success(request, "Activity type created!")
            return redirect("activity_list")
    else:
        form = ActivityTypeForm()
    return render(request, "planner/activity_form.html", {"form": form})


def activity_delete(request, activity_id):
    activity = get_object_or_404(ActivityType, id=activity_id)
    if request.method == "POST":
        activity.delete()
        messages.success(request, "Activity type deleted.")
        return redirect("activity_list")
    return render(
        request, "planner/activity_confirm_delete.html", {"activity": activity}
    )


def session_update(request):
    """
    Handles create, update, and delete for training sessions.
    Expected POST data:
    - plan_id
    - date
    - activity_type_id
    - notes (optional)
    - completed (optional, boolean-ish)
    - action (save, delete)
    """
    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        date_str = request.POST.get("date")
        activity_type_id = request.POST.get("activity_type_id")
        action = request.POST.get("action")

        plan = get_object_or_404(Plan, id=plan_id)
        activity_type = get_object_or_404(ActivityType, id=activity_type_id)

        # Try to find existing session
        session = TrainingSession.objects.filter(
            plan=plan, date=date_str, activity_type=activity_type
        ).first()

        if action == "delete":
            if session:
                session.delete()
                messages.success(request, "Session removed.")
            else:
                messages.warning(request, "Nothing to delete.")

        elif action == "save":
            notes = request.POST.get("notes", "")
            completed = request.POST.get("completed") == "on"

            if session:
                session.notes = notes
                session.completed = completed
                session.save()
                messages.success(request, "Session updated.")
            else:
                TrainingSession.objects.create(
                    plan=plan,
                    date=date_str,
                    activity_type=activity_type,
                    notes=notes,
                    completed=completed,
                )
                messages.success(request, "Session added.")

    # Redirect back to the plan
    return redirect("plan_detail", plan_id=plan_id)


def sessions_bulk_update(request):
    """
    Bulk update sessions for a given date.
    Sets which activities are active for that day.
    """
    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        date_str = request.POST.get("date")
        selected_activities = request.POST.getlist("activities")  # List of activity IDs

        plan = get_object_or_404(Plan, id=plan_id)

        # Get all existing sessions for this date
        existing_sessions = TrainingSession.objects.filter(plan=plan, date=date_str)
        existing_activity_ids = set(str(s.activity_type.id) for s in existing_sessions)
        selected_set = set(selected_activities)

        # Delete sessions that are no longer selected
        for session in existing_sessions:
            if str(session.activity_type.id) not in selected_set:
                session.delete()

        # Add new sessions for newly selected activities
        for activity_id in selected_set:
            if activity_id not in existing_activity_ids:
                activity_type = get_object_or_404(ActivityType, id=activity_id)
                TrainingSession.objects.create(
                    plan=plan,
                    date=date_str,
                    activity_type=activity_type,
                    completed=False,
                )

        messages.success(request, f"Activities updated for {date_str}")
        return redirect("plan_detail", plan_id=plan_id)

    return redirect("index")
