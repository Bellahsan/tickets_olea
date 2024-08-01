from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from django.core.cache import cache
from django.contrib import admin

from .models import Ticket, User, TypeTicket


# Create your views here.


def redirecttohome(request):
    return redirect('/')


def clear_cache(request):
    cache.clear()
    return redirect('/')


@staff_member_required
def index(request):
    context = admin.site.each_context(request)
    return render(request, 'website/index.html', context)


class TicketsView(PermissionRequiredMixin, TemplateView):
    permission_required = "webiste.can_view_tickets"
    template_name = 'website/tickets.html'
    model = Ticket

    def get(self, request, *args, **kwargs):
        context_original = self.get_context_data(**kwargs)
        tickets = Ticket.objects.all()
        context_perso = {
            'tickets': tickets
        }
        context = {**context_original, **context_perso}
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        }


def tickets_datatable(request):
    pass


class UsersView(PermissionRequiredMixin, TemplateView):
    permission_required = "webiste.can_view_users"
    template_name = 'website/users.html'
    model = User

    def get(self, request, *args, **kwargs):
        context_original = self.get_context_data(**kwargs)
        users = User.objects.all()
        context_perso = {
            'users': users
        }
        context = {**context_original, **context_perso}
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        }


def tickets_datatable(request):
    pass


class TypesTicketsView(PermissionRequiredMixin, TemplateView):
    permission_required = "webiste.can_view_types_tickets"
    template_name = 'website/types.html'
    model = TypeTicket

    def get(self, request, *args, **kwargs):
        context_original = self.get_context_data(**kwargs)
        types = TypeTicket.objects.all()
        context_perso = {
            'types': types
        }
        context = {**context_original, **context_perso}
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        }


def types_tickets_datatable(request):
    pass
