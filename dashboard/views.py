from django.shortcuts import render

# Create your views here.
def home(request):
	data = {}
	data['breadcrumb'] = [('Home','active','')]
	data['tabs'] = [('Uploads',365),('Mobiles',64),('Url',345),('DNS',435),('Applications',543),('Activities',3534)]

	return render(request, 'dashboard/home.html', data)