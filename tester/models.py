from django.db import models
from pxe.models import *

class TestName(models.Model):
    name = models.CharField(max_length=100)
    available = models.BooleanField()
    
    def __str__(self):
        return self.name
    
class SystemVersion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TestLog(models.Model):
    STATUS_CHOICES = (
        ('R', 'Requested'),
        ('S', 'Sent'),
        ('D', 'Done'),
        ('E', 'Error'),
        )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    system = models.ForeignKey(System)
    test_name = models.ForeignKey(TestName)
    warnings = models.IntegerField(default=0)
    infos = models.IntegerField(default=0)
    errors = models.IntegerField(default=0)
    version = models.ForeignKey(SystemVersion, null=True)

    def __str__(self):
        return "%s %s" % (self.test_name, self.status)

class InfoLine(models.Model):
    type = models.CharField(max_length=1)
    log = models.ForeignKey(TestLog)
    text = models.CharField(max_length=100)

    def __str__(self):
        return "%s for %s" % (self.type, self.log)

from django.contrib import admin
admin.site.register(SystemVersion)
admin.site.register(TestName)
admin.site.register(TestLog)
admin.site.register(InfoLine)
