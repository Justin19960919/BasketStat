from django.apps import AppConfig


class UsrsConfig(AppConfig):
    name = 'usrs'
    
    def ready(self):
        import usrs.signals