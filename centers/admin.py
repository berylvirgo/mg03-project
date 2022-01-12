from django.contrib import admin
from .models import Message, Alert


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "subject", "body", "timestamp")


# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Alert)