from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from .categories import CHOICES_FOR_CATEGORIES


class Notification(models.Model):

    title = models.CharField(unique=True, blank=False, max_length=128)
    description = RichTextUploadingField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=CHOICES_FOR_CATEGORIES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notification', kwargs={'pk': self.object.id})

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)


class Response(models.Model):
    text = models.TextField(blank=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    responded_user = models.ForeignKey(User, on_delete=models.CASCADE)