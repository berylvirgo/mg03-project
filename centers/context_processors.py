from django.http import JsonResponse

from centers.views import email
from .models import *


def messages_and_alerts(request):
    if request.user.is_authenticated:
        context = {
            'message_alerts': Message.objects.filter(
                user=request.user, recipients=request.user
            ).order_by("-timestamp")[0:4],
            'email': email,
            'message_count': Message.objects.filter(
                user=request.user, recipients=request.user, read=False
            ).order_by("-timestamp").count(),
            'alerts': Alert.objects.filter(
                user=request.user
            ).order_by("-created")[0:3],
            'alert_count': Alert.objects.filter(
                user=request.user, is_read=False
            ).order_by("-created").count(),
        }
        return context
    else:
        return {
            'users': User.objects.all()
        }
