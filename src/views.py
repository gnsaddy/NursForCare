from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ExtendedUserCreationForm, ServiceBookingForm, ExtendedVendorCreationForm
from .models import City, Vendor, Chaperone


class Index(TemplateView):
    template_name = 'index.html'


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')

        user = auth.authenticate(email=email, password=pass1)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request,
                           'Please enter a correct username and password. Note that both fields may be '
                           'case-sensitive.')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


def userRegistration(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            ven = form.cleaned_data.get('user')
            print(ven)
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}.')
            return redirect('login')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'registration/userRegistration.html', {'form': form})


def vendorRegistration(request):
    if request.method == 'POST':
        form1 = ExtendedVendorCreationForm(request.POST)
        if form1.is_valid():
            ven = form1.cleaned_data.get('vendor')
            print(ven)
            form1.save()
            email = form1.cleaned_data.get('email')

            messages.success(request, f'Account created for {email}.')
            return redirect('login')
    else:
        form1 = ExtendedVendorCreationForm()
    return render(request, 'registration/vendorRegistration.html', {'form1': form1})


@login_required()
def bookingService(request):
    if request.method == 'POST':
        bookingForm = ServiceBookingForm(request.POST, request.FILES)

        if bookingForm.is_valid():
            instance = bookingForm.save(commit=False)
            instance.holder = request.user
            instance.save()
            username = bookingForm.cleaned_data.get('patient')
            messages.success(request, f'Booking done successfully for {username}.')
            return redirect('serviceBooking')
    else:
        bookingForm = ServiceBookingForm()
    return render(request, '../templates/patient/serviceBooking.html', {'bookingForm': bookingForm})


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'booking/city_dropdown_list_options.html', {'cities': cities})


def load_services(request):
    city_id = request.GET.get('city')
    services = Vendor.objects.filter(city_id=city_id).order_by('name')

    return render(request, 'booking/city_dropdown_list_options.html', {'services': services})


def logout(request):
    auth.logout(request)
    return redirect('index')
