from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ExtendedUserCreationForm, UserProfileForm, ServiceBookingForm


class Index(TemplateView):
    template_name = 'index.html'


class PageNotFound(TemplateView):
    template_name = 'include/404.html'


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        pass1 = request.POST.get('password1')

        user = auth.authenticate(username=username, password=pass1)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.warning(request,
                             'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


def userRegistration(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        userProfileForm = UserProfileForm(request.POST)
        if form.is_valid() and userProfileForm.is_valid():
            user = form.save()
            user_profile = userProfileForm.save(commit=False)
            user_profile.holder = user
            user_profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('login')
    else:
        form = ExtendedUserCreationForm()
        userProfileForm = UserProfileForm()
    return render(request, 'registration/userRegistration.html', {'form': form, 'userProfileForm': userProfileForm})


@login_required()
def bookingService(request):
    if request.method == 'POST':
        bookingForm = ServiceBookingForm(request.POST)

        if bookingForm.is_valid():
            instance = bookingForm.save(commit=False)
            instance.holder = request.user
            instance.save()
            username = bookingForm.cleaned_data.get('patient')
            messages.success(request, f'Booking done successfully for {username}.')
            messages.success(request, 'Your contact has been successfully created!')
            return redirect('index')
    else:
        bookingForm = ServiceBookingForm()
    return render(request, 'booking/bookService.html', {'bookingForm': bookingForm})


def logout(request):
    auth.logout(request)
    return redirect('index')
