from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
#SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
ZIP_DIR_NAME = "pcap_uploads"
# Create your views here.
def upload(request):
	data = {}
	data['breadcrumb'] = [('Home','',''),('Upload','active','')]
	data['tabs'] = [('Uploads',365),('Mobiles',64),('Url',345),('DNS',435),('Applications',543),('Activities',3534)]
	if request.method == 'POST' and request.FILES['myPcap']:
		myfile = request.FILES['myPcap']
		print(myfile)
		fs = FileSystemStorage()
		filename = myfile.name
		filepath = fs.save(os.path.join(ZIP_DIR_NAME,myfile.name), myfile)
		print(filename)
		print(filepath)
		#data['path'].append(filename)
		#uploaded_file_url = fs.url(filepath)
		#abs_file_url = SITE_ROOT.replace('upload','')+uploaded_file_url
		#file_stat = list(os.stat(abs_file_url))
	return render(request, 'upload/upload.html', data)