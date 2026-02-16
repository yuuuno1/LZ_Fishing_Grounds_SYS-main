from django.db import models

# Create your models here.
class AuditLog(models.Model):
    audit_name = models.CharField(max_length=250, null=False)
    audit_action = models.CharField(max_length=250, null=False)
    audit_module = models.CharField(max_length=250, null=False)
    audit_timestamp  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.audit_action