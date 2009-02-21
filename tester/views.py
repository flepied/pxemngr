import re
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from forms import UploadFileForm
from pxe.common import *
from tester.models import *

def upload_file(request, logid):
    print 'upload_file', logid
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        mac = get_mac(request)
        s = get_object_or_404(System, macaddress__mac=simplify_mac(mac))
        log = get_object_or_404(TestLog, id=logid)
        if form.is_valid():
            log.status = 'D'
            log.save()
            print 'valid', log.status
            handle_uploaded_file(request.FILES['file'], log.id)
            process_file(log)
            return HttpResponse("uploaded", mimetype="text/plain")
        else:
            log.status = 'E'
            log.save()
            print 'invalid form', log.status
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})

def get_filename(id):
    return '%s/%d.log' % (settings.TEST_UPLOAD_DIR, id)

def handle_uploaded_file(f, id):
    destination = open(get_filename(id), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

info_regexp = re.compile('^([IEWSVT]): (.*)')

def add_info_line(type, text, log):
    i = InfoLine(type=type, text=text, log=log)
    i.save()
    return i

def process_file(log):
    info = 0
    error = 0
    warning = 0
    for line in open(get_filename(log.id)).readlines():
        res = info_regexp.search(line)
        if res:
            if res.group(1) == 'I':
                info = info + 1
                add_info_line(res.group(1), res.group(2), log)
            elif res.group(1) == 'E':
                error = error + 1
                add_info_line(res.group(1), res.group(2), log)
            elif res.group(1) == 'W':
                warning = warning + 1
                add_info_line(res.group(1), res.group(2), log)
            elif res.group(1) == 'V':
                version = res.group(2)
                try:
                    v = SystemVersion.objects.get(name=version)
                except SystemVersion.DoesNotExist:
                    v = SystemVersion(name=version)
                    v.save()
                log.version = v
    log.warnings = warning
    log.infos = info
    log.errors = error
    log.save()
    
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
    else:
        log = None
    print "%s (%s) -> %s (%s)" % (s.name, mac, name, str(log))
    return render_to_response(name + settings.TEST_SUFFIX, {'testname': name, 'system': s.name, 'log': log})

def logs(request, verid):
    version = get_object_or_404(SystemVersion, id=verid)
    logs = TestLog.objects.filter(version=version).order_by('-date')
    return render_to_response('logs.html', {'logs': logs, 'version': version})    

def log(request, logid):
    log = get_object_or_404(TestLog, id=logid)
    infos = InfoLine.objects.filter(log=log).order_by('id')
    return render_to_response('log.html', {'log': log, 'infos': infos})

def content(request, logid):
    log = get_object_or_404(TestLog, id=logid)
    filename = get_filename(log.id)
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def index(request):
    versions = SystemVersion.objects.all().order_by('-id')
    systems = System.objects.all().order_by('name')
    testnames = TestName.objects.filter(available=True).order_by('name')
    return render_to_response('index.html', {'versions': versions,
                                             'systems': systems,
                                             'testnames': testnames})    

def script(request, name):
    return render_to_response(name + settings.TEST_SUFFIX, {'testname': name, 'system': 'system', 'log': None})

def system(request, sysid):
    s = get_object_or_404(System, id=sysid)
    testlogs = TestLog.objects.filter(system=s).order_by('-date')
    logs = Log.objects.filter(system=s).order_by('-date')[0:10]
    return render_to_response('system.html', {'system': s, 'logs': testlogs, 'boots': logs})    

def testname(request, tstid):
    name = get_object_or_404(TestName, id=tstid)
    logs = TestLog.objects.filter(test_name=name).order_by('-date')
    return render_to_response('tests.html', {'logs': logs, 'testname': name})    

# views.py ends here
