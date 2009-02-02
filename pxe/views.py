#---------------------------------------------------------------
# Project         : pxemngr
# File            : views.py
# Copyright       : 2009 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 13:54:41 2009
# Purpose         : http logic
#---------------------------------------------------------------

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from common import *
from models import *

def localboot(request, mac):
    system = get_object_or_404(System, macaddress__mac=simplify_mac(mac))
    set_next_boot(system, settings.PXE_LOCAL)
    return HttpResponse("Next boot set to local", mimetype="text/plain")

def profile(request, mac):
    system = get_object_or_404(System, macaddress__mac=simplify_mac(mac))
    log = Log.objects.filter(system=system).order_by('-date')[0]
    return HttpResponse(log.boot_name.name, mimetype="text/plain")
