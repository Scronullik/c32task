from django.core import management

from apscheduler.schedulers.background import BackgroundScheduler


def cleanup_sessions():
    """
    Функция выполняющая запуск задачи переодической очистки устаревших сессий.
    Сессии очищаются путём запуска встроенной комманды django: ./manage.py clearsession.
    Возраст сессий задаётся в параметре SESSION_COOKIE_AGE настроек проекта.
    Это не очищает кэш redis. Кэш redis очищается по TTL.
    """
    def task():
        """Cleanup expired sessions by using Django management command."""
        management.call_command("clearsessions", verbosity=0)
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, 'interval', minutes=1440)  # one day
    scheduler.start()
