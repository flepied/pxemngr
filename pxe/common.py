#---------------------------------------------------------------
# Project         : pxemngr
# File            : common.py
# Copyright       : 2009-2010 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 19:03:58 2009
#---------------------------------------------------------------

"""Common functions used by scripts and web logic."""

import sys
import os
import re
import settings
from pxe.models import *

_MAC_REGEXP = re.compile('^.*\s([0-9a-f:]+)\s.*', re.I)
_IP_REGEXP = re.compile('^([0-9.]+).*\s[0-9a-f:]+\s.*', re.I)

def ip_to_mac(ip):
    """Lookup a MAC address from an IPV4 address on a live Linux system."""
    for line in open('/proc/net/arp').readlines():
        if line.find(ip) != -1:
            res = _MAC_REGEXP.search(line)
            if res:
                return res.group(1)
    return None

def mac_to_ip(mac):
    """Lookup an IPV4 address from a MAC address on a live Linux system."""
    mac = mac.upper()
    for line in open('/proc/net/arp').readlines():
        if line.find(mac) != -1:
            res = _IP_REGEXP.search(line)
            if res:
                return res.group(1)
    return None

def get_mac(request):
    """Returns a MAC address corresponding to the IPV4 address of the remote host of the request."""
    mac = ip_to_mac(request.META['REMOTE_ADDR'])
    if not mac:
        print 'no mac for', request.META['REMOTE_ADDR']
        raise Http404
    return mac
    
def error(str):
    """Print an error and exit with a return code of 1."""
    sys.stderr.write(str + '\n')
    sys.exit(1)

def simplify_mac(s):
    """Remove : or - between hexa numbers for a MAC address. Always returns the address in lowercase"""
    ss = s.replace('-', '')
    sss = ss.replace(':', '')
    if len(sss) != 12:
        print 'simplify_mac: invalid length (not 12)', sss, len(sss)
        raise ValueError
    return sss.lower()

def mac2filename(m):
    """Returns a filename using the naming convention used by PXE: 01-<mac address separated by - >."""
    s = '01-'
    for i in range(0, 10, 2):
        s = s + '%s-' % m[i:i+2]
    s = s + '%s' % m[10:12]
    return s

def mac2path(mac):
    """Returns the path of the MAC or IPV4 mask in the file system."""
    if len(mac) == 12:
        return '%s/%s' % (settings.PXE_ROOT, mac2filename(mac))
    else:
        return '%s/%s' % (settings.PXE_ROOT, mac)
    
def create_symlink(src, dst):
    """Creates a symlink removing the destination if it exists before."""
    if os.path.exists(dst):
        os.unlink(dst)
    os.symlink(src, dst)
    
def set_next_boot(system, name, abort=True):
    """Sets next boot symlinks in the PXE and stores the value in the database."""
    try:
        boot_name = BootName.objects.get(name=name)
    except BootName.DoesNotExist:
        if abort:
            error('Boot name %s not defined' % name)
        else:
            raise BootName.DoesNotExist

    prof = '%s/%s%s' % (settings.PXE_PROFILES, boot_name.name, settings.PXE_SUFFIX)
    
    name_dst = '%s/%s' % (settings.PXE_ROOT, system.name)
    create_symlink(prof, name_dst)
    for m in MacAddress.objects.filter(system=system):
        dst = mac2path(m.mac)
        create_symlink(system.name, dst)
        
    if system.name == 'default':
        create_symlink(prof, '%s/default' % (settings.PXE_ROOT))

    log = Log(system=system, boot_name=boot_name)
    log.save()

def simplify_ip(ip):
    """Returns a string containing the hexadecimal representation of an IPV4 address or a sub-part."""
    l = ip.split('.')
    s = ''
    for e in l:
        s = s + '%02X' % int(e)
    return s

if __name__ == "__main__":
    import unittest
    
    class commonTest(unittest.TestCase):
    
        def test1(self):
            """simplify_ip test."""
            return self.assertEqual(simplify_ip('10.34'), '0A22')

        def test2(self):
            """mac2filename test."""
            return self.assertEqual(mac2filename('001b38710ab6'), '01-00-1b-38-71-0a-b6')

        def test3(self):
            """simplify_mac test."""
            return self.assertEqual(simplify_mac('00:1b:38:71:0a:b6'), '001b38710ab6')

        def test4(self):
            """simplify_mac test."""
            return self.assertRaises(ValueError, lambda: simplify_mac('00:1b:38:71:0a'))

    unittest.main()

# common.py ends here
