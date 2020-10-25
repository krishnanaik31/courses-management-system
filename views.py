import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import OrderForm, InterestForm, RegisterForm
from .models import Topic, Course, Student, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    if request.session.get('last_login', default=None) is None:
        login_time = "Your last login was more than one hour ago"
    else:
        login_time = request.session.get('last_login')
    return render(request, 'myapp/index.html', {'top_list': top_list, 'login_time': login_time})
    # top_list = Topic.objects.all().order_by('id')[:10]
    # courses = Course.objects.all().order_by('-price')[0:5]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of topics: ' + '</p>'
    # response.write(heading1)
    # for element in top_list:
    #     para = '<p>' + str(element.id) + ': ' + str(element) + '</p>'
    #     response.write(para)
    # heading = '<p>' + 'List of courses: ' + '</p>'
    # response.write(heading)
    # for course in courses:
    #     para = '<p>' + str(course) + ':'
    #     response.write(para)
    #     if course.for_everyone == 1:
    #         response.write(' This Course is For Everyone!')
    #     else:
    #         response.write(' This Course is Not For Everyone! </p>')
    # return response


def about(request):
    # response = HttpResponse()
    # response.write(heading)
    no_times = 1
    response = render(request, 'myapp/about.html', {'visit': no_times})
    if request.COOKIES.get("about_visits", None) is None:
        response.set_cookie('about_visits', no_times, expires=300)
    else:
        num_hit = request.COOKIES.get("about_visits")
        num_hit = int(num_hit)+1
        response = render(request, 'myapp/about.html', {'visit': num_hit})
        response.set_cookie('about_visits', num_hit, expires=300)
    return response


def detail(request, top_no):
    response = HttpResponse()
    try:
        top_list = Topic.objects.get(id=top_no)
    except Topic.DoesNotExist:
        raise Http404("404 : Topic cannot be found")
    course_list = Course.objects.filter(topic__name=top_list)
    context = {'topic': top_list, 'course_list': course_list}
    return render(request, 'myapp/detail.html', context)


def courses(request):
    course_list = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'course_list': course_list})


def place_order(request):
    msg = ''
    course_list = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                if order.course.price > 150.00:
                    Course.discount(order.course)
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'course_list': course_list})


def coursedetail(request, course_id):
    course_detail = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == '1':
                course_detail.interested_to = course_detail.interested_to + 1
                course_detail.save()
            return redirect('myapp:index')
    else:
        form = InterestForm()
    return render(request, 'myapp/coursedetail.html', {'form': form, 'course_detail': course_detail})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                user_object = User.objects.get(username=username)
                time = datetime.datetime.now()
                request.session['last_login'] = str(time)
                request.session['u_id'] = user_object.id
                # request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:my_account'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    del request.session['u_id']
    request.session.flush()
    return redirect('myapp:index')


@login_required
def myaccount(request):
    if request.user.is_authenticated:
        student_details = Student.objects.filter(username=request.user).values()
        if student_details:
            order_details = Order.objects.filter(student__user_ptr__first_name=request.user.first_name)
            course_details = Student.objects.filter(username=request.user).values('interested_in__name')
            return render(request, 'myapp/myaccount.html', {'student_details': student_details,
                          'order_details': order_details, 'course_details': course_details})
        else:
            msg = 'You are not a registered student!'
            return render(request, 'myapp/myaccount.html', {'msg': msg})
    else:
        return render(request, 'myapp/login.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:login')
    form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
