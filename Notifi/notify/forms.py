from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from django_filters import ModelMultipleChoiceFilter

from .models import Notification, Response

class NotificationForm(forms.ModelForm):


    class Meta:
        model = Notification
        description = forms.CharField(widget=CKEditorUploadingWidget())
        fields = [
            'title',
            'category',
            'description',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("description")

        heading = cleaned_data.get('title')
        if heading == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = (
            'text','notification','responded_user'
        )
        widgets = {
            'notification': forms.HiddenInput(),
            'responded_user': forms.HiddenInput(),
        }