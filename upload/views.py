from django.shortcuts import render
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
import os
from datetime import datetime
#SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PCAP_UPLOAD = "pcap_uploads"
MEDIA_PATH =  os.path.join(os.getcwd(),'media')

from .models import xDPI_upload_history
# Create your views here.
def upload(request):
	data = {}
	data['breadcrumb'] = [('Home','',''),('Upload','active','')]
	data['upload_history_columns'] = [field.name for field in xDPI_upload_history._meta.fields]
	data['upload_history'] = xDPI_upload_history.objects.all().order_by('-upload_date')
	uploads = xDPI_upload_history.objects.all().order_by('-upload_date')
	paginator = Paginator(uploads,5)
	page = request.GET.get('page')
	data['datas'] = paginator.get_page(page)

	if request.method == 'POST' and request.FILES['myPcap']:
		myfile = request.FILES['myPcap']
		fs = FileSystemStorage()
		#filename = myfile.name
		filepath = fs.save(os.path.join(PCAP_UPLOAD,myfile.name), myfile)
		filename = filepath.split(os.sep)[-1]
		upload_db_update = xDPI_upload_history(
			file_name=filename,
			file_size=os.path.getsize(os.path.join(MEDIA_PATH,filepath)),
			upload_date=datetime.now(tz=timezone.utc)
		).save()
		#data['path'].append(filename)
		#uploaded_file_url = fs.url(filepath)
		#abs_file_url = SITE_ROOT.replace('upload','')+uploaded_file_url
		#file_stat = list(os.stat(abs_file_url))
	return render(request, 'upload/upload.html', data)