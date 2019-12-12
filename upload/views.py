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
		data['scan_path'] = os.path.join(MEDIA_PATH,filepath)
	return render(request, 'upload/upload.html', data)

def scanner(request):

	def xDPIsession(scan_path):
		data = []
		try:
			from datetime import datetime
			from dpkt.pcap import Reader
			from dpkt.ethernet import Ethernet
			from socket import inet_ntoa
			with open(scan_path,'rb') as pf:
				dpkt_file_object = False
				try:dpkt_file_object = Reader(pf)
				except Exception as err:
					dpkt_file_object = False
					#print("[-] pcap corruption detected : {}".format(pcap_path))
				if dpkt_file_object:
					#print("[+] pcap's health fine : {}".format(pcap_path))
					for ts, payload in dpkt_file_object:
						t1, p = ts, payload
						t = datetime.fromtimestamp(t1).strftime("%Y-%m-%d %H:%M:%S")
						eth = False
						try:eth = Ethernet(payload)
						except:eth = False
						if eth:
							if eth.type == 2048:
								ip = eth.data
								src_ip = inet_ntoa(ip.src)
								dst_ip = inet_ntoa(ip.dst)
								data.append({
										'src_ip' : src_ip,
										'dst_ip' : dst_ip,
									})
		except Exception as err:
			print(err)
		return data

	data = {}
	data['breadcrumb'] = [('Home','',''),('Upload','',''),('Scanner','active','')]

	if request.method == 'POST' and 'scan_path' in request.POST and 'scanner' in request.POST:
		scan_path = request.POST.get('scan_path')
		scanner_type = request.POST.get('scanner')
		print(scan_path, scanner_type)
		if scanner_type == 'session':
			sessions = xDPIsession(scan_path)
			data['datas'] = sessions

	return render(request, 'upload/scan.html', data)
