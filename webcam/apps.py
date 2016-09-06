from django.apps import AppConfig


class WebCamConfig(AppConfig):
    name = 'webcam'

    def ready(self):
        import webcam.signals  # noqa
