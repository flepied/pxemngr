#---------------------------------------------------------------
# Project         : tester
# File            : forms.py
# Version         : $Id$
# Author          : Frederic Lepied
# Created On      : Sun Feb  8 16:24:02 2009
# Purpose         : 
#---------------------------------------------------------------

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

# forms.py ends here
