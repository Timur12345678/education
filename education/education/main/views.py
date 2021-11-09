from django.shortcuts import render
from main.models import SiteUser
import random
import requests
from django.shortcuts import redirect


def get_random_number(random_len):#0000 -- 9999
    random_len = int(random_len)
    a = pow(10, random_len)
    b = pow(10, random_len-1)
    n = random.randint(b,a)
    return n

def send_messahe(phone, sms):
    sms_domain = 'https://smsc.kz/sys/send.php'
    sms_params = {
        'login': 'timaedgarov',
        'psw':'hacklink98',
        'mes': sms,
        'fmt':3,
        'phones': phone
    }
    r= requests.post(sms_domain, data=sms_params)
    print(r.status_code)
    print(r.json())
    print(phone)
    print(sms)

def mainHandler(request):

    user_id = request.session.get('user_id', None)
    active_user = None

    if user_id:
        active_user = SiteUser.objects.get(id = int(user_id))

    return render(request, 'index.html',{ 'user_id': user_id,  'active_user': active_user})
# Create your views here.

def loginHandler(request):
    post_error = ''
    if request.POST:
        phone= request.POST.get('phone','')
        password= request.POST.get('password')
        if phone and password:
            site_user = SiteUser.objects.filter(phone=phone).filter(password=password)
            if site_user:
                site_user = site_user[0]
                request.session['user_id'] = site_user.id
                return redirect('/')
            else:
                post_error = 'USER NOT FOUND'
        else:
            post_error = 'Arguments ERROR'

    return render(request, 'login.html',{'post_error': post_error  })



def logoutHandler(request):
    return render(request, 'logout.html',{ })

def registerHandler(request):
    if request.POST:
        phone= request.POST.get('phone','')
        if phone:
            if len(phone) == 11:
                site_user = SiteUser.objects.filter(phone=phone)
                if site_user:
                    new_site_user = site_user[0]
                    new_site_user.password = get_random_number(6)
                    new_site_user.save()
                    message = 'You login code:' + str(new_site_user.password)
                    send_messahe(phone, message)
                    return redirect('/login/')
                else:
                    new_site_user = SiteUser()
                    new_site_user.phone = phone
                    new_site_user.password = get_random_number(6)
                    new_site_user.save()
                    message = 'You login code:' + str(new_site_user.password)
                    send_messahe(phone, message)
                    return redirect('/login/')
            else:
                print('number format error')

        else:
            print('NO ARGS')
    return render(request, 'register.html',{ })

