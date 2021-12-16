from django.core import management

from apscheduler.schedulers.background import BackgroundScheduler


def cleanup_sessions():
    def task():
        """Cleanup expired sessions by using Django management command."""
        management.call_command("clearsessions", verbosity=0)
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, 'interval', minutes=1440)
    scheduler.start()
