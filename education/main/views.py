from django.shortcuts import render
from main.models import SiteUser
import random
import requests
from django.shortcuts import redirect
from main.models import *
import re
from hashlib import md5

email_regex = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")
phone_regexp = re.compile(r'^77[0-9]{9}$')
iin_regexp = re.compile(r'[0-9]{12}$')


def get_random_number(random_len):  # 0000 -- 9999
    random_len = int(random_len)
    a = pow(10, random_len)
    b = pow(10, random_len - 1)
    n = random.randint(b, a)
    return n


def send_messahe(phone, sms):
    sms_domain = 'https://smsc.kz/sys/send.php'
    sms_params = {
        'login': 'timaedgarov',
        'psw': 'hacklink98',
        'mes': sms,
        'fmt': 3,
        'phones': phone
    }
    r = requests.post(sms_domain, data=sms_params)
    print(r.status_code)
    print(r.json())
    print(phone)
    print(sms)


def mainHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None

    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    courses = Course.objects.all()
    course_count = Course.objects.count()

    return render(request, 'index.html',
                  {'user_id': user_id, 'active_user': active_user, 'courses': courses, 'course_count': course_count})


def courseHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None

    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))


    all_courses = Course.objects.all()
    all_categories = CourseCategory.objects.all()

    return render(request, 'course.html', {'user_id': user_id, 'active_user': active_user,
                                           'all_courses':all_courses, 'all_categories': all_categories})



def courseItemHandler(request, course_id):
    active_lesson_number = request.GET.get('lesson',1)
    user_id = request.session.get('user_id', None)
    active_user = None

    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    course = Course.objects.get(id=course_id)
    course_lesson_count = CourseItem.objects.filter(course_id = course_id).count()
    lesson_counts = range(1, course_lesson_count + 1)

    course_items = CourseItem.objects.filter(course__id = course_id)
    first_course_item: None
    paragraphs =[]
    if course_items:
        first_course_item = course_items[0]



        paragraphs = CourseItemParagraph.objects.filter(course_item__id = first_course_item.id)
    return render(request, 'course_item.html', {'user_id': user_id, 'active_user': active_user,
                                                'course': course, 'course_lesson_count': course_lesson_count,
                                                'first_course_item':first_course_item, 'paragraphs': paragraphs,
                                                'lesson_counts': lesson_counts, 'active_lesson_number': active_lesson_number})


def loginHandler(request):
    post_error = ''
    if request.POST:
        login = request.POST.get('login', '')  # phone or email
        password = request.POST.get('password')
        if login and password:

            temp_hash = md5()
            temp_hash.update(password.encode())
            password_hash = temp_hash.hexdigest()

            site_user = SiteUser.objects.filter(phone=login).filter(password=password_hash)
            if not site_user:
                site_user = SiteUser.objects.filter(email=login).filter(password=password_hash)

            if site_user:
                site_user = site_user[0]
                request.session['user_id'] = site_user.id
                return redirect('/')
            else:
                post_error = 'USER NOT FOUND'
        else:
            post_error = 'Arguments ERROR'

    return render(request, 'login.html', {'post_error': post_error})


def logoutHandler(request):
    request.session['user_id'] = None
    return redirect('/')
    # return render(request, 'logout.html', {})


def registerHandler(request):
    if request.POST:
        phone = request.POST.get('phone', '')
        if phone:
            if len(phone) == 11:
                site_user = SiteUser.objects.filter(phone=phone)
                if site_user:
                    new_site_user = site_user[0]
                    old_password = str(get_random_number(6))

                    print(old_password)

                    password_hash = md5()
                    password_hash.update(old_password.encode())
                    new_password = password_hash.hexdigest()

                    new_site_user.password = new_password
                    new_site_user.save()
                    message = 'You login code:' + str(old_password)
                    send_messahe(phone, message)
                    return redirect('/login/')
                else:
                    new_site_user = SiteUser()
                    new_site_user.phone = phone
                    old_password = str(get_random_number(6))

                    print(old_password)

                    password_hash = md5()
                    password_hash.update(old_password.encode())
                    new_password = password_hash.hexdigest()

                    new_site_user.password = new_password
                    new_site_user.save()
                    message = 'You login code:' + str(old_password)
                    send_messahe(phone, message)
                    return redirect('/login/')
            else:
                print('number format error')

        else:
            print('NO ARGS')
    return render(request, 'register.html', {})


def editHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    post_errors = []

    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    if request.POST:
        last_name = request.POST.get('last_name', '')
        first_name = request.POST.get('first_name', '')
        middle_name = request.POST.get('middle_name', '')
        iin = request.POST.get('iin', '')
        email = request.POST.get('email', '')

        active_user.last_name = last_name
        active_user.first_name = first_name
        active_user.middle_name = middle_name
        if iin:
            if iin_regexp.match(iin):
                active_user.iin = iin
            else:
                post_errors.append('IIN format error')

        if email:
            if email_regex.match(email):
                email_users = SiteUser.objects.filter(email=email)
                if email_users:
                    email_user = email_users[0]
                    if email_user.id == active_user.id:
                        pass
                    else:
                        post_errors.append('This email already registered')
                else:
                    active_user.email = email

            else:
                post_errors.append('Email format error')
        active_user.save()

    return render(request, 'edit.html', {'user_id': user_id, 'active_user': active_user, 'post_errors': post_errors})
