#---------------------------------------------------------------
# Project         : pxemngr
# File            : Makefile
# Copyright       : 2009 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 13:54:41 2009
# Purpose         : build rules
#---------------------------------------------------------------

VERSION=0.1

all:
	@echo "use 'make dist' to build a tar ball"
	@exit 1

dist: clean
	cd ..; tar jcvf pxemngr-$(VERSION).tar.bz2 --exclude .svn --exclude pxe.db pxemngr

clean:
	find . -name '*~' -o -name '*.pyc'|xargs rm -f

# Makefile ends here
