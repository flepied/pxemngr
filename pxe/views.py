#---------------------------------------------------------------
# Project         : pxemngr
# File            : views.py
# Copyright       : 2009-2010 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 13:54:41 2009
# Purpose         : http logic
#---------------------------------------------------------------

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from pxe.common import *
from pxe.models import *

def get_system(request, mac):
    try:
        return System.objects.get(macaddress__mac=simplify_mac(mac))
    except System.DoesNotExist:
        pass

    addr = request.META['REMOTE_ADDR']
    l = map(lambda x: '%02x' % int(x), addr.split('.'))
    for i in range(len(l), 1, -1):
        try:
            return System.objects.get(macaddress__mac=''.join(l[0:i]))
        except System.DoesNotExist:
            pass
    raise Http404

def localboot1(request):
    return localboot(request, get_mac(request))
    
def localboot(request, mac):
    try:
        system = System.objects.get(macaddress__mac=simplify_mac(mac))
        set_next_boot(system, settings.PXE_LOCAL)
    except System.DoesNotExist:
        fn = '%s/%s' % (settings.PXE_ROOT, mac2filename(simplify_mac(mac)))
        create_symlink('%s/%s%s' % (settings.PXE_PROFILES, settings.PXE_LOCAL, settings.PXE_SUFFIX), fn)
    
    return HttpResponse("Next boot set to local", mimetype="text/plain")

def profile1(request):
    return profile(request, get_mac(request))
    
def profile(request, mac):
    system = get_system(request, mac)
    log = Log.objects.filter(system=system).order_by('-date')[0]
    return HttpResponse(log.boot_name.name, mimetype="text/plain")
