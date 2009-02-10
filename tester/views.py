from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from forms import UploadFileForm
from pxe.common import *
from tester.models import *

def upload_file(request):
    print 'upload_file'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        mac = get_mac(request)
        s = get_object_or_404(System, macaddress__mac=simplify_mac(mac))
        logs = TestLog.objects.filter(system=s, status='S').order_by('date')
        if len(logs) == 0:
            raise Http404
        log = logs[0]
        if form.is_valid():
            log.status = 'D'
            log.save()
            print 'valid', log.status
            handle_uploaded_file(request.FILES['file'], log.id)
            return HttpResponse("uploaded", mimetype="text/plain")
        else:
            log.status = 'E'
            log.save()
            print 'invalid form', log.status
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})

def handle_uploaded_file(f, id):
    destination = open('%s/%d.log' % (settings.TEST_UPLOAD_DIR, id), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def next_test1(request):
    mac = get_mac(request)
    return next_test(request, mac)

def next_test(request, mac):
    smac = simplify_mac(mac)
    s = get_object_or_404(System, macaddress__mac=smac)
    name = 'wait'
    logs = TestLog.objects.filter(system=s, status='R').order_by('date')
    if logs and len(logs) > 0:
        log = logs[0]
        name = log.test_name.name
        log.status = 'S'
        log.save()
    return render_to_response(name + settings.TEST_SUFFIX, {'testname', name})
    
# views.py ends here
