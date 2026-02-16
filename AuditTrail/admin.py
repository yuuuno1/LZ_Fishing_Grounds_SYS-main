from django.contrib import admin

from AuditTrail.models import AuditLog

# Register your models here.
admin.site.register(AuditLog)