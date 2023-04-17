from datetime import datetime, date, timedelta

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth import login as lg
from django.contrib.auth import logout
from django.db.models import Q
from comparis_web.models import Properties
from django.core.paginator import Paginator, EmptyPage


def home(request):
    properties = Properties.objects.filter(onlinestatus__isnull=False)
    return render(request, 'home.html', context={'properties': properties})


def properties_views(request):
    if request.method == 'POST':
        p_type = request.POST.get('p_type')
        town_postcode = request.POST.get('town_postcode')
        price = request.POST.get('price')
        room = request.POST.get('room')
        duration = request.POST.get('duration')
        status = request.POST.get('status')
        search_date = request.POST.get('date')
        queryset = Properties.objects.all().order_by('-publish_date')
        if p_type:
            queryset = queryset.filter(propertytypetext=p_type)

        if town_postcode:
            queryset = queryset.filter(postalcode=town_postcode)

        if price:
            queryset = queryset.filter(price__lte=int(price))

        if room:
            queryset = queryset.filter(room__lte=room)
        if status:
            if status == 'any':
                queryset = queryset.filter().all()
            elif status == 'online':
                queryset = queryset.filter(onlinestatus__isnull=False)
            elif status == 'offline':
                queryset = queryset.filter(onlinestatus__isnull=True)

        if search_date:
            queryset = queryset.filter(publish_date__gte=search_date)

        if duration:
            start_date = date.today() - timedelta(days=int(duration))
            end_date = date.today()
            query = Q(publish_date__range=(start_date, end_date))
            queryset = queryset.filter(query)

        try:
            page_number = int(request.POST.get('page', '1'))
        except:
            page_number = int(request.GET.get('page', '1'))
        items_per_page = 50
        paginator = Paginator(queryset, items_per_page)
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            data = {
                'success': False,
                'message': 'Invalid page number',
            }
            return JsonResponse(data, status=400)

        data = {
            'success': True,
            'data': list(page_obj.object_list.values()),
            'page_obj': {
                'number': page_obj.number,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'num_pages': page_obj.paginator.num_pages,
                'per_page': page_obj.paginator.per_page,
            }
        }
        if page_obj.has_next():
            data['page_obj']['next_page_number'] = page_obj.next_page_number()
        else:
            data['page_obj']['next_page_number'] = None
        return JsonResponse(data)
    else:
        return render(request, 'properties_listing.html')


def detail_view(request, id):
    property = Properties.objects.get(prop_id=id)
    image_urls = property.imageurls.split('||')
    return render(request, 'detail_page.html', context={'property': property, 'image_url': image_urls})


def login(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        password = request.POST.get('pass')
        user = authenticate(username=user_name, password=password)
        if user is not None:
            lg(request, user)
            messages.info(request, f"You are now logged in as {user_name}.")
            return redirect("home")
        else:
            messages.warning(request, "Invalid username or password.")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        try:
            user = User.objects.create_user(username=user_name, email=email, password=password)
            user.save()
            messages.success(request, 'Registration Completed...!')
            return render(request, 'login.html')
        except:
            messages.info(request, 'User Already Exist....!')
            return render(request, 'signup.html')
    return render(request, 'signup.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'example@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("/password_reset/done/")
            else:
                messages.INFO(request, 'Invalid Email Address..')
                return redirect('password_reset')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html",
                  context={"password_reset_form": password_reset_form})


def logout_view(request):
    logout(request)
    return redirect('home')
