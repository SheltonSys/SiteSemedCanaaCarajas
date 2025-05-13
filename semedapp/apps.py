from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver


class SemedappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'semedapp'




@receiver(connection_created)
def set_storage_engine(sender, connection, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute("SET default_storage_engine=INNODB;")
        cursor.execute("SET NAMES 'utf8mb4';")
        cursor.execute("SET CHARACTER SET utf8mb4;")
        cursor.execute("SET collation_connection = 'utf8mb4_general_ci';")
