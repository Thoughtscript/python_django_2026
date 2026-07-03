from django.apps import AppConfig


class DjangoExample(AppConfig):
    name = "djangoexample"
    verbose_name = "djangoexample"

    def ready(self):
        # explicitly import signals
        import djangoexample.signals