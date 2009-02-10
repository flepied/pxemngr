#---------------------------------------------------------------
# Project         : pxemngr
# File            : common.py
# Copyright       : 2009 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 19:03:58 2009
# Purpose         : common functions used by scripts and web logic.
#---------------------------------------------------------------

import sys
import os
import re
import settings
from models import *

IP_REGEXP = re.compile('^.*\s([0-9A-F:]+)\s.*')

def mac_to_ip(mac):
    for line in open('/proc/net/arp').readlines():
        if line.find(mac) != -1:
            res = IP_REGEXP.search(line)
            if res:
                return res.group(1)
    return False

def get_mac(request):
    mac = mac_to_ip(request.META['REMOTE_ADDR'])
    if not mac:
        raise Http404
    print 'get_mac', mac
    return mac
    
def error(str):
    sys.stderr.write(str + '\n')
    sys.exit(1)

def simplify_mac(s):
    '''Remove : or - between hexa numbers for a MAC address. Always return the address in lowercase'''
    print 'simplify_mac', s
    ss = s.replace('-', '')
    sss = ss.replace(':', '')
    if len(sss) != 12:
        print 'invalid length (not 12)', sss, len(sss)
        raise ValueError
    return sss.lower()

def mac2filename(m):
    s = ''
    for i in range(0, 10, 2):
        s = s + '%s-' % m[i:i+2]
    s = s + '%s' % m[10:12]
    return s

def set_next_boot(system, name, abort=True):
    try:
        boot_name = BootName.objects.get(name=name)
    except BootName.DoesNotExist:
        if abort:
            error('Boot name %s not defined' % name)
        else:
            raise BootName.DoesNotExist
        
    for m in MacAddress.objects.filter(system=system):
        dst = '%s/01-%s' % (settings.PXE_ROOT, mac2filename(m.mac))
        if os.path.exists(dst):
            os.unlink(dst)
        os.symlink('%s/%s%s' % (settings.PXE_PROFILES, boot_name.name, settings.PXE_SUFFIX),
                   dst)
    log = Log(system=system, boot_name=boot_name)
    log.save()

# common.py ends here
