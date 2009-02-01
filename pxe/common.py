#---------------------------------------------------------------
# Project         : pxemngr
# File            : common.py
# Version         : $Id$
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 19:03:58 2009
# Purpose         : 
#---------------------------------------------------------------

import sys
import os
import settings
from pxe.models import *

def error(str):
    sys.stderr.write(str + '\n')
    sys.exit(1)

def simplify_mac(s):
    '''Remove : or - between hexa numbers for a MAC address. Always return the address in lowercase'''
    ss = s.replace('-', '')
    sss = ss.replace(':', '')
    if len(sss) != 12:
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
        dst = '%s/%s' % (settings.PXE_ROOT, mac2filename(m.mac))
        if os.path.exists(dst):
            os.unlink(dst)
        os.symlink('%s/%s%s' % (settings.PXE_PROFILES, boot_name.name, settings.PXE_SUFFIX),
                   dst)
    log = Log(system=system, boot_name=boot_name)
    log.save()

# common.py ends here
