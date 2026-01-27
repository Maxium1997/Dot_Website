from django.apps import AppConfig


class BadmintonCourtManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'badminton_court_management'

    def ready(self):
        # 在啟動時匯入訊號
        import badminton_court_management.signals
