import django_filters
from django import forms
from django.http import request

from django_filters import FilterSet, DateFromToRangeFilter, ChoiceFilter, ModelChoiceFilter
from django_filters.widgets import RangeWidget

from .models import Notification,Response, User

def get_notfs_by_user(request):
    if request is None:
        return Notification.objects.none()
    return Notification.objects.filter(creator=request.user)


class NotificationFilter(FilterSet):
    title = django_filters.ModelChoiceFilter(
        queryset=get_notfs_by_user,
        empty_label="All Notifications",
        label="Notifications",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Notification
        fields = ['title']
