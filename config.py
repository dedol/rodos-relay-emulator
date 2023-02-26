import os

class Config(object):
    AUTH_USERNAME = os.getenv('AUTH_USERNAME', 'admin')
    AUTH_PASSWORD = os.getenv('AUTH_PASSWORD', 'admin')
    IMPULSE_TIMER_SEC = int(os.getenv('IMPULSE_TIMER_SEC', 10))
    SCHEDULER_TIMEZONE = 'Europe/Moscow'