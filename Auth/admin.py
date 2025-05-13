from django.contrib import admin

from Auth.models import Admin , SuperAdmin , Utilisateur

# Register your models here.
admin.site.register(SuperAdmin)

admin.site.register(Admin)

admin.site.register(Utilisateur)