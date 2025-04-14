# TODO: Utility functions
import os
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("You must be logged in to access this page.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def is_admin(user_id: int) -> bool:
    """
    Check if the user is an admin based on their Discord ID.

    Args:
        user_id (int): The Discord user ID.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    admin_ids = os.getenv("ADMIN_USER_IDS", "").split(",")
    return str(user_id) in admin_ids