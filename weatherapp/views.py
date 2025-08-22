import requests
import datetime
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def index(request):
    city = request.GET.get('city')
    weather_data = {}
    forecast_data = []
    if city:
        api_key = "842b6757a0cd289ff6438f1031170c74"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response2 = requests.get(forecast_url).json()
        if response.get('cod') == 200:
            weather_data = {
                'city': city,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'humidity': response['main']['humidity'],
                'wind': response['wind']['speed']
            }
            for i in range(0,len(response2['list']),8):
                day = response2['list'][i]
                day_str = day['dt_txt']
                day_obj = datetime.datetime.strptime(day_str,"%Y-%m-%d %H:%M:%S")
                day_name = day_obj.strftime('%A')
                forecast_data.append({
                    'date':day['dt_txt'],
                    'day':day_name,
                    'temperature':day['main']['temp'],
                    'description':day['weather'][0]['description'],
                    'icon':day['weather'][0]['icon'],
                    'humidity': day['main']['humidity'],
                    'wind': day['wind']['speed']
                })
        else:
            weather_data = {'error': 'city not found'}
        
    return render(request, 'home.html', {'weather': weather_data,'forecast':forecast_data})
def loginuser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
def signup(request):
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpass = request.POST.get('confirm_password')
        if password!=confirmpass:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'username already exists'})
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect('home')
    else:
        return render(request, 'signup.html')
def logoutuser(request):
    logout(request)
    return render(request,'login.html')
    