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
    
# models.py ends here
