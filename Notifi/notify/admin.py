from django.contrib import admin

# Register your models here.
from .models import Notification,Response


admin.site.register(Notification)
admin.site.register(Response)


