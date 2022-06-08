from .models import Notification


def create_notification(user, content, connection_type, connection):
    title = f"connection request {connection_type}"

    notification = Notification.objects.create(
        user = user,
        title = title,
        content = content,
        connection = connection 
    )

    return notification
