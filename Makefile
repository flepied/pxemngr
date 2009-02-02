VERSION=0.1

all:
	@echo "use 'make dist' to build a tar ball"
	@exit 1

dist: clean
	cd ..; tar jcvf pxemngr-$(VERSION).tar.bz2 --exclude .svn --exclude pxe.db pxemngr

clean:
	find . -name '*~' -o -name '*.pyc'|xargs rm -f

# Makefile ends here
