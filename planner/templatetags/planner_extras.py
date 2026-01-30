from datetime import date

from django import template

register = template.Library()


@register.filter
def get_session(session_map, date_obj):
    """
    Returns the inner dictionary for a given date, or None.
    Usage: {{ session_map|get_session:date_obj }}
    """
    if not session_map:
        return None
    return session_map.get(date_obj)


@register.filter
def get_activity_session(date_sessions, activity_type_id):
    """
    Returns the session for a given activity type from the date_sessions dict.
    Usage: {{ date_sessions|get_activity_session:activity.id }}
    """
    if not date_sessions:
        return None
    return date_sessions.get(activity_type_id)


@register.filter
def is_past(date_obj):
    return date_obj < date.today()
