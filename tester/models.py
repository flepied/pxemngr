from django.db import models
from pxe.models import *

class TestName(models.Model):
    name = models.CharField(max_length=100)
    available = models.BooleanField()

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
