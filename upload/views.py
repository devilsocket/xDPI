from django.shortcuts import render

# Create your views here.
def upload(request):
	data = {}
	data['breadcrumb'] = [('Home','',''),('Upload','active','')]
	data['tabs'] = [('Uploads',365),('Mobiles',64),('Url',345),('DNS',435),('Applications',543),('Activities',3534)]

	return render(request, 'upload/upload.html', data)