from django.core import management

from apscheduler.schedulers.background import BackgroundScheduler


def cleanup_sessions():
    """
    This function which performs the task of periodically clearing expired sessions.
    Sessions are cleared by running django's built-in command: ./manage.py clearsession.
    The age of the session is set in the SESSION_COOKIE_AGE parameter of the project's settings.
    This does not clear the redis cache. The redis cache is cleared by TTL.
    """
    def task():
        """Cleanup expired sessions by using Django management command."""
        management.call_command("clearsessions", verbosity=0)
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, 'interval', minutes=1440)  # one day
    scheduler.start()
