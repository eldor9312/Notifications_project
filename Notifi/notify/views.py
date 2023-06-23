from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import FormMixin

from .filters import NotificationFilter
from .forms import NotificationForm, ResponseForm
from .models import Notification, Response


class NotificationsList(ListView):
    model = Notification
    template_name = 'all_notifications.html'
    context_object_name = 'all_notfs'
    ordering = '-creation_date'
    paginate_by = 2


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class NotificationDetailed(FormMixin, DetailView):
    model = Notification
    template_name = "notification_detailed.html"
    context_object_name = "notification_detailed"
    form_class = ResponseForm

    def get_success_url(self):
        return reverse('notification', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(NotificationDetailed, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.id)
        notification = Notification.objects.get(pk=self.kwargs['pk'])
        context['form'] = ResponseForm(initial={
            'notification': notification,
            'responded_user': user,
        })

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(NotificationDetailed, self).form_valid(form)

class NotificationCreate(CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'notification_create.html'

    def form_valid(self, form, pk):
        notf = form.save(commit=False)
        notf.creator = self.request.user
        notf.notification = pk
        return super().form_valid(form)


class NotificationDelete(DeleteView):
    model = Notification
    template_name = 'notification_delete.html'
    success_url = reverse_lazy('notifications_list')


# class MyNotifications(ListView):
#     model = User,Notification,Response
#     template_name = 'personal_page.html'
#     context_object_name = 'mynotifications'
#
# class ResponseCreate(CreateView):
#     model = Response
#     form_class = ResponseForm
#     context_object_name = 'responses'
#     template_name = 'all_notifications.html'
#     def form_valid(self, form):
#         response = form.save(commit=False)
#         response.responded_user = self.request.user
#         response.notification = self.request.notification.id
#         return super().form_valid(form)



def get_profile_page(request):
    user = request.user
    all_notfs = Notification.objects.filter(creator=user)
    notfs = []
    all_resps = []
    f = NotificationFilter(request.GET, queryset=all_notfs, request=request)
    for i in all_notfs:
        notfs.append(i)
        curr = Response.objects.filter(notification=i)
        for j in curr:
            all_resps.append(j)

    context = {
        'notifications': notfs,
        'responses': all_resps,
        'filter': f,
    }

    return render(request, 'personal_page.html',context)


@login_required
def response_to_notification_accept(request, pk):
    response = Response.objects.get(pk=pk)
    user_email_to = response.responded_user.email
    send_mail(
        subject=f"{request.user.username}",
        message="Your response has been claimed!",
        from_email="prodaldeda@yandex.ru",
        recipient_list=[user_email_to]
    )
    response.delete()
    return redirect("personal_page")


@login_required
def response_to_notification_reject(instance, pk):
    response = Response.objects.get(pk=pk)
    response.delete()
    return redirect("personal_page")



