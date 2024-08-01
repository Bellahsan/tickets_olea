from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group

from website.models import User

class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        return super(CustomAdminSite, self).index(request, extra_context)

AdminSite.index_template = 'main_index.html'
custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(Group)
custom_admin_site.register(User)
