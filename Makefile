#---------------------------------------------------------------
# Project         : pxemngr
# File            : Makefile
# Copyright       : 2009 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 13:54:41 2009
# Purpose         : build rules
#---------------------------------------------------------------

VERSION=0.7.1

bindir=/usr/bin
libdir=/usr/share/pxemngr
etcdir=/etc

all:
	@echo "use 'make dist' to build a tar ball."
	@echo "use 'make install' to install the files in the system."
	@exit 1

install:
	mkdir -p $(DESTDIR)$(bindir) $(DESTDIR)$(libdir)/pxe $(DESTDIR)$(libdir)/tester $(DESTDIR)$(etcdir)
	install pxe/pxemngr $(DESTDIR)$(bindir)/pxemngr
	install -m 644 pxe/pxemngr.conf $(DESTDIR)$(etcdir)/pxemngr.conf
	install *.py $(DESTDIR)$(libdir)/
	install pxe/*.py pxe/{addsystem,dpysystem,nextboot,syncbootnames,delsystem} $(DESTDIR)$(libdir)/pxe/
	install tester/*.py tester/{dpytest,nexttest,synctestnames} $(DESTDIR)$(libdir)/tester/

dist: clean
	cd ..; tar jcvf pxemngr-$(VERSION).tar.bz2  --exclude .git --exclude pxe.db pxemngr

clean:
	find . -name '*~' -o -name '*.pyc'|xargs rm -f

# Makefile ends here
