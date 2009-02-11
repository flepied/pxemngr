#---------------------------------------------------------------
# Project         : pxemngr
# File            : models.py
# Copyright       : 2009 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 13:54:41 2009
# Purpose         : describe sql tables.
#---------------------------------------------------------------

from django.db import models

class System(models.Model):
    name = models.CharField(max_length=100)

class MacAddress(models.Model):
    mac = models.CharField(max_length=12)
    system = models.ForeignKey(System)
    
class BootName(models.Model):
    name = models.CharField(max_length=100)
    available = models.BooleanField()
    
class Log(models.Model):
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    system = models.ForeignKey(System)
    boot_name = models.ForeignKey(BootName)

from django.contrib import admin
admin.site.register(System)
admin.site.register(MacAddress)
admin.site.register(BootName)
admin.site.register(Log)

# models.py ends here
