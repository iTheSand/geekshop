from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser


def login(request):
    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {
        'title': 'вход',
        'login_form': login_form,
        'next': next
    }

    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print('success')
                return render(request, 'authapp/success_send_massage.html')
            else:
                print('failed')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': 'регистрация',
        'form': register_form
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {
        'title': 'редактирование',
        'edit_form': edit_form,
        'profile_form': profile_form
    }

    return render(request, 'authapp/edit.html', content)


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    subject = f'Подтверждение учетной записи от {settings.EMAIL_HOST_USER.split("@")[0]}'

    massage = f'Ссылка для активации: {settings.BASE_URL}{verify_link}'

    return send_mail(subject, massage, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)


def verify(request, email, activation_key):
    user = ShopUser.objects.get(email=email)
    if user.activation_key == activation_key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return render(request, 'authapp/verification.html')
