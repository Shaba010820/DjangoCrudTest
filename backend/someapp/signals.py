from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Users
from channels.layers import get_channel_layer


@receiver(post_save, sender=Users)
def send_welcome_notification(sender, instance, created, **kwargs):
    if created:
        print("🔥 Сигнал сработал! Отправляем уведомление...")

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',  # Название группы, которая будет получать уведомления
            {
                'type': 'notification_send',  # Имя метода в потребителе WebSocket
                'message': f'👤 Новый пользователь зарегистрирован: {instance.username}'  # Сообщение
            }
        )